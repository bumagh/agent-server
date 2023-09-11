#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from app.libs.error_code import Success
from app.dao.AdminLogDAO import AdminLogDAO
from app.core.utils import paginate

adminLog = Blueprint('adminLog', __name__, url_prefix='/auth.AdminLog')


@adminLog.route("/index", methods=['GET'])
def admin_log():
    page, size = paginate()
    quickSearch = request.args.get("quickSearch")
    logs = AdminLogDAO.queryByPage(page, size,quickSearch)
    return Success(logs)
