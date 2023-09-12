# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/4/16.
"""
from app.core.db import db
from app.libs.enums import ClientTypeEnum
from app.model.baAdmin import BaAdmin
from app.model.baAdminGroupAccess import BaAdminGroupAccess


class AdminDao():
    # 更改密码
    @staticmethod
    def change_password(uid, old_password, new_password):
        identity = BaAdmin.get_or_404(user_id=uid)  # 找到一个
        if identity.check_password(old_password):
            identity_list = BaAdmin.query.filter(
                BaAdmin.type.in_([
                    ClientTypeEnum.USERNAME.value,
                    ClientTypeEnum.EMAIL.value,
                    ClientTypeEnum.MOBILE.value]),
                BaAdmin.id == uid
            ).all()
            with db.auto_commit():
                for item in identity_list:
                    item.update(commit=False, password=new_password)

    # 重置密码
    @staticmethod
    def reset_password(uid, password):
        identity_list = BaAdmin.query.filter(
            BaAdmin.type.in_([
                ClientTypeEnum.USERNAME.value,
                ClientTypeEnum.EMAIL.value,
                ClientTypeEnum.MOBILE.value]),
            BaAdmin.id == uid
        ).all()
        with db.auto_commit():
            for item in identity_list:
                item.update(commit=False, password=password)

    # 更新用户
    @staticmethod
    def update_user(uid, form):
        with db.auto_commit():
            # 第1步: 获取用户信息
            user = BaAdmin.query.filter_by(id=uid).first_or_404()
            # 第2步: 核对需修改的信息(用户名、手机号、邮箱)
            if hasattr(form, BaAdmin.username.key) and user.username != form.username:
                BaAdmin.abort_repeat(username=form.username, msg='该用户名已被使用，请重新输入新的用户名')
                user.update(commit=False, username=form.username)
            if hasattr(form, BaAdmin.mobile.key) and user.mobile != form.mobile:
                BaAdmin.abort_repeat(mobile=form.mobile, msg='手机号已被使用，请重新输入新的手机号')
                user.update(commit=False, mobile=form.mobile)
            if hasattr(form, BaAdmin.email.key) and user.email != form.email:
                BaAdmin.abort_repeat(email=form.email, msg='邮箱已被使用，请重新输入新的邮箱号')
                user.update(commit=False, email=form.email)
            if hasattr(form, BaAdmin.password.key):
                # 生成随机盐
                salt = AdminDao.generate_salt()
                # 使用盐对密码进行哈希
                credential = AdminDao.get_credential(password=form.password, salt=salt)
                user.update(commit=False, salt=salt, password=credential)
            if hasattr(form, BaAdmin.nickname.key) and user.nickname != form.nickname:
                user.update(commit=False, nickname=form.nickname)
            if hasattr(form, BaAdmin.avatar.key) and user.avatar != form.avatar:
                user.update(commit=False, avatar=form.avatar)
            if hasattr(form, BaAdmin.status.key) and user.status != form.status:
                user.update(commit=False, status=form.status)

            # 操作权限数组
            if hasattr(form, 'group_arr'):
                for gid in form.group_arr:
                    if gid > 0:
                        AdminDao.operation_admin_group(uid=uid, group_id=gid)

    @staticmethod
    def operation_admin_group(**kwargs):
        instance = BaAdminGroupAccess.query.filter_by(**kwargs).first()
        if instance:
            return
        else:
            BaAdminGroupAccess.create(**kwargs)

    # 新增用户
    @staticmethod
    def create_admin(data_dict):
        group_arr = data_dict['group_arr']
        # 删除字段
        if 'group_arr' in data_dict:
            del data_dict['group_arr']
        admin_info = BaAdmin.create(**data_dict)
        uid = admin_info.id
        for group_id in group_arr:
            BaAdminGroupAccess.create(uid=uid, group_id=group_id)

    # 获取用户列表
    @staticmethod
    def get_admin_list(page, size):
        paginator = db.session.query(BaAdmin.id, BaAdmin.username, BaAdmin.nickname, BaAdmin.avatar, BaAdmin.email,
                                     BaAdmin.mobile, BaAdmin.last_login_time, BaAdmin.last_login_ip, BaAdmin.motto,
                                     BaAdmin.status, BaAdmin.update_time, BaAdmin.create_time) \
            .paginate(page=page, per_page=size, error_out=True)
        return paginator

    @staticmethod
    def delete_element(ids):
        '''删除用户'''
        with db.auto_commit():
            BaAdmin.query.filter(BaAdmin.id.in_(ids)).delete()
            BaAdminGroupAccess.query.filter(BaAdminGroupAccess.uid.in_(ids)).delete()

    @staticmethod
    def get_credential(password, salt):
        import hashlib
        salted_password = password + salt
        md5_hash = hashlib.md5(salted_password).hexdigest()
        return md5_hash

    # 生成随机盐
    @staticmethod
    def generate_salt(length=16):
        import string
        import random
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
