#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from app.libs.error_code import Success
from app.dao.AdminLogDAO import AdminLogDAO
from app.core.utils import paginate

adminLog = Blueprint('adminLog', __name__, url_prefix='/auth.AdminLog')


@adminLog.route("/index", methods=['GET'])
def admin_log():
    page,size = paginate()
    logs = AdminLogDAO.queryByPage(page,size)
    return Success(logs)
