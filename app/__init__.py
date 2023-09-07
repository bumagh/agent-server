# _*_ coding: utf-8 _*_
import logging
import os

from flask import Flask
from app.core.db import db
from app.core.error import APIException, ServerError, RepeatException
from werkzeug.exceptions import HTTPException
from app.core.logger import apply_request_log
from sqlalchemy.exc import IntegrityError

from app.api import register_blueprint

from app.extensions.default_view import apply_default_view

CONFIG_NAME_MAPPER = {
    'development': 'config.Development.cfg',
    'testing': 'config.Testing.cfg',
    'production': 'config.Production.cfg'
}


def create_app(flask_config_name=None):
    '''' create flask app '''

    ## Load Config
    env_flask_config_name = os.getenv('FLASK_CONFIG')
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = 'development'
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name

    try:
        if CONFIG_NAME_MAPPER[flask_config_name] is None:
            return None
    except KeyError:
        return None

    ## Creat app
    app = Flask(__name__)
    app.config.from_pyfile(CONFIG_NAME_MAPPER[flask_config_name])
    app.config.SWAGGER_UI_JSONEDITOR = True
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

    register_blueprint('app.api', app)
    register_plugin(app)

    return app


def register_plugin(app):
    apply_json_encoder(app)  # JSON序列化
    apply_cors(app)  # 应用跨域扩展，使项目支持请求跨域
    connect_db(app)  # 连接数据库
    handle_error(app)  # 统一处理异常

    # Debug模式(以下为非必选应用，且用户不可见)
    apply_default_view(app)  # 应用默认路由
    if app.config['DEBUG']:
        apply_request_log(app)  # 打印请求日志


def set_logger(app):
    # logging.getLogger('flask_cors').level = logging.DEBUG
    # logging.getLogger('elasticsearch').level = logging.WARNING
    logging.basicConfig(format=app.config['LOGGER_FORMAT'], level=app.config['LOGGER_LEVEL'])


def apply_json_encoder(app):
    from app.core.json_encoder import JSONEncoder
    app.json_encoder = JSONEncoder


def apply_cors(app):
    from flask_cors import CORS
    cors = CORS()
    cors.init_app(app, resources={"/*": {"origins": "*"}})


def connect_db(app):
    db.init_app(app)
    #  初始化使用
    with app.app_context():  # 手动将app推入栈
        db.create_all()  # 首次模型映射(ORM ==> SQL),若无则建表


def handle_error(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            return APIException(code=e.code, error_code=1007, msg=e.description)
        elif isinstance(e, IntegrityError) and 'Duplicate entry' in e.orig.errmsg:
            return RepeatException(msg='数据的unique字段重复')
        else:
            if not app.config['DEBUG']:
                return ServerError()  # 未知错误(统一为服务端异常)
            else:
                raise e
