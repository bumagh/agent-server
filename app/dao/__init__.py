from flask_sqlalchemy import SQLAlchemy
from app.model import init_model
from werkzeug.utils import cached_property

class DaoPool:
    sqlDAO = None
    esDAO = None

    def __init__(self):
        pass

    def init_app(self, app):
        # db init

        self.sqlDAO = SQLAlchemy(app)
        init_model(self.sqlDAO)


daoPool = DaoPool()
