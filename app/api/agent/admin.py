#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Blueprint

from app.core.error import Success
from app.core.utils import paginate
from app.dao.admin import AdminDao

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/list', methods=['GET'])
def get_user_list():
    '''查询用户列表(分页)'''
    page, size = paginate()
    rv = AdminDao.get_admin_list(page, size)
    return Success(rv)

@admin.route('/<int:uid>', methods=['GET'])
def get_user(uid):
    '''查询用户信息'''
    user = AdminDao.query.filter_by(id=uid).first_or_404()
    return Success(user)