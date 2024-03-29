# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/4/8.
  print输出字体颜色: https://www.cnblogs.com/easypython/p/9084426.html
"""
import json
import time
import re
from functools import wraps
from flask import g, Response, request, _request_ctx_stack
from app.libs.enums import OperTyepEnum

__author__ = 'Allen7D'

REG_XP = r'[{](.*?)[}]'
OBJECTS = ['user', 'response', 'request']


class Logger(object):
    template = None  # 默认消息模版

    def __init__(self, module='', template=None, type=OperTyepEnum.OTHER):
        '''
        :param module: 红图模块(红图中文名)
        :param template: 消息模版
        :param type: 操作类型
        '''
        if template:
            self.template = template
        elif self.template is None:
            raise Exception('template must not be None!')

        self.module = module
        self.type = type.value if type in OperTyepEnum else OperTyepEnum.OTHER.value
        self.message = ''
        self.response = None
        self.user = None

    def __call__(self, func):
        @wraps(func)
        def wrap(*args, **kwargs):
            response = func(*args, **kwargs)
            self.response = response
            self.user = g.user
            if not self.user:
                raise Exception('Logger must be used in the login state')
            self.message = self._parse_template()
            # self.write_log()
            return response

        return wrap

    # 解析自定义模板
    def _parse_template(self):
        message = self.template
        total = re.findall(REG_XP, message)
        for it in total:
            assert '.' in it, '%s中必须包含 . ,且为一个' % it
            i = it.rindex('.')
            obj = it[:i]
            assert obj in OBJECTS, '%s只能为user, response, request中的一个' % obj
            prop = it[i + 1:]
            if obj == 'user':
                item = getattr(self.user, prop, '')
            elif obj == 'response':
                item = getattr(self.response, prop, '')
            else:
                item = getattr(request, prop, '')
            message = message.replace('{%s}' % it, str(item))
        return message


# 记录每次请求的性能
def apply_request_log(app):
    @app.before_request
    def request_cost_time():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5f" % (time.time() - g.request_start_time)

    @app.after_request
    def log_response(res):
        message = '[%s] -> [%s] from:%s costs:%.3f ms' % (
            request.method,
            request.path,
            request.remote_addr,
            float(g.request_time()) * 1000
        )
        req_body = request.get_json() if request.get_json() else {}
        data = {
            'path': _request_ctx_stack.top.request.view_args,
            'query': request.args,
            'body': req_body
        }
        message += '\n\"data\": ' + json.dumps(data, indent=4, ensure_ascii=False)
        # 设置颜色开始(至多3类参数，以m结束)：\033[显示方式;前景色;背景色m
        print('\033[0;34m')
        if request.method in ('GET', 'POST', 'PUT', 'DELETE'):
            print(message)
        print('\033[0m')  # 终端颜色恢复
        return res




# 基于ip解析真实地址
def parse_location_by_ip(ip):
    '''
    :param ip: ip地址
    :return: ip所在的省市
    '''
    if ip == '127.0.0.1' or ip.startswith('192.168.'):
        return "内网IP"
    from app.libs.httper import HTTP
    try:
        url = 'http://whois.pconline.com.cn/ipJson.jsp?{0}&json=true'.format(ip)
        json_data = HTTP.get(url)
        return '{0} {1}'.format(json_data['pro'], json_data['city'])
    except Exception:
        return '获取地理位置异常 {ip}'.format(ip=ip)
