#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Blueprint
from app.core.utils import jsonify
from app.core.error import Success
from app.core.utils import paginate
from app.dao.admin import AdminDao
from app.dao.admin_group_access import AdminGroupAccessDao
from app.model.baAdmin import BaAdmin
from app.model.baAdminGroup import BaAdminGroup
from app.service.admin import AdminService

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/list', methods=['GET'])
def get_user_list():
    '''查询用户列表(分页)'''
    page, size = paginate()
    rv = AdminDao.get_admin_list(page, size)
    rv = AdminService.option_group_field(rv)
    return Success(rv)


@admin.route('/edit/<int:uid>', methods=['GET'])
def get_user(uid):
    '''查询用户信息'''
    user = BaAdmin.query.filter_by(id=uid).first_or_404()
    groupid, groupname = AdminGroupAccessDao.get_user_admin_group_info(user['id'])
    user = jsonify(user)
    user['group_arr'] = groupid
    user['group_name_arr'] = groupname
    return Success(user)


@admin.route('/rule_list/<int:id>', methods=['GET'])
def rule_list(id):
    '''查询分组信息'''
    query = BaAdminGroup.query
    if id > 0:
        query = BaAdminGroup.query.filter_by(id=id).first_or_404()
    else:
        query = query.all()
    return Success(query)
