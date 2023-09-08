#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from app.libs.error_code import Success

adminLog = Blueprint('adminLog', __name__, url_prefix='/auth.AdminLog')


@adminLog.route("/index", methods=['GET'])
def admin_log():
    limit = request.args.get('limit', type=int)
    print(limit)
    page = request.args.get('page', type=int)
    print(page)
    return Success("limit={} and page = {}".format(limit, page))
