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
        # 第1步: 核对需修改的信息(用户名、手机号、邮箱)
        identity_infos = []
        if (hasattr(form, 'username')):
            identity_infos.append(
                {'identifier': form.username, 'type': ClientTypeEnum.USERNAME.value,
                 'msg': '该用户名已被使用，请重新输入新的用户名'})
        if (hasattr(form, 'mobile')):
            identity_infos.append(
                {'identifier': form.mobile, 'type': ClientTypeEnum.MOBILE.value,
                 'msg': '手机号已被使用，请重新输入新的手机号'})
        if (hasattr(form, 'email')):
            identity_infos.append(
                {'identifier': form.email, 'type': ClientTypeEnum.EMAIL.value,
                 'msg': '邮箱已被使用，请重新输入新的邮箱号'})
        # 第2步: 修改用户信息
        with db.auto_commit():
            # 第2.1步: 获取用户信息
            user = BaAdmin.query.filter_by(id=uid).first_or_404()
            credential = BaAdmin.get_credential(user_id=uid)
            # 第2.2步: 修改用户昵称
            if hasattr(form, 'nickname'):
                user.update(commit=False, nickname=form.nickname)
            # 第2.3步: 依次修改用户身份信息(用户名、手机号、邮箱)
            for item in identity_infos:
                BaAdmin.abort_repeat(identifier=item['identifier'], msg=item['msg'])
                BaAdmin.update_identity(
                    commit=False, user_id=uid, identifier=item['identifier'], credential=credential, type=item['type']
                )

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
        return {
            'total': paginator.total,
            'current_page': paginator.page,
            'items': paginator.items
        }

    # 删除用户
    @staticmethod
    def delete_element(ids):
        with db.auto_commit():
            BaAdmin.query.filter(BaAdmin.id.in_(ids)).delete()
            BaAdminGroupAccess.query.filter(BaAdminGroupAccess.uid.in_(ids)).delete()
