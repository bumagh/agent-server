#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint
from app.libs.error_code import Success

demo = Blueprint('demo', __name__, url_prefix='/demo')


@demo.route('/test', methods=['GET'])
def get_user_list():
    return Success("hello!")
