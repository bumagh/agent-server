#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Blueprint, request
from app.core.utils import jsonify
from app.core.error import Success
from app.core.utils import paginate
from app.dao.admin import AdminDao
from app.dao.admin_group_access import AdminGroupAccessDao
from app.model.baAdmin import BaAdmin
from app.model.baAdminGroup import BaAdminGroup
from app.service.admin import AdminService
from app.service.file import FileService
from app.validators.forms import IDCollectionValidator, UploadFileValidator, CreateAdminValidator

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


@admin.route('/add', methods=['POST'])
def add_user():
    form = CreateAdminValidator().get_data('type')
    AdminDao.create_admin(form)
    return Success()


@admin.route('/del/<string:ids>', methods=['DELETE'])
def del_user():
    '''删除用户信息'''
    ids = IDCollectionValidator().nt_data.ids
    AdminDao.delete_element(ids)
    return Success(error_code=2)


@admin.route('/rule_list/<int:id>', methods=['GET'])
def rule_list(id):
    '''查询分组信息'''
    query = BaAdminGroup.query
    if id > 0:
        query = BaAdminGroup.query.filter_by(id=id).first_or_404()
    else:
        query = query.all()
    return Success(query)


@admin.route('/upload', methods=['POST'])
def post_file():
    '''文件上传'''
    validator = UploadFileValidator().nt_data
    filename = FileService(file=validator.file).save()
    return Success(msg='{} 保存成功'.format(filename), error_code=1)
