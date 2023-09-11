# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/4/16.
"""
from app.core.db import db
from app.libs.enums import ClientTypeEnum
from app.model.baAdmin import BaAdmin

__author__ = 'Allen7D'

from app.model.baAdminGroup import BaAdminGroup
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

    # 更新头像
    @staticmethod
    def set_avatar(id, avatar):
        '''
        :param id: 用户id
        :param avatar: 头像url
        :return:
        '''
        with db.auto_commit():
            user = BaAdmin.get(id=id)
            user._avatar = avatar

    # 更新身份
    @staticmethod
    def update_identity(commit=True, user_id=None, identifier=None, credential=None, type=None):
        identity = BaAdmin.get(user_id=user_id, type=type)
        if identity:
            identity.update(commit=commit,
                            identifier=identifier, credential=credential)
        else:
            BaAdmin.create(commit=commit, user_id=user_id, type=type,
                           identifier=identifier, credential=credential)

    # 删除用户
    @staticmethod
    def delete_user(uid):
        user = BaAdmin.query.filter_by(id=uid).first_or_404()
        with db.auto_commit():
            BaAdmin.query.filter_by(user_id=user.id).delete(commit=False)
            user.delete(commit=False)

    # 更换权限组
    @staticmethod
    def change_group(uid, group_id):
        user = BaAdmin.get_or_404(id=uid)
        user.update(group_id=group_id)

    # 获取用户列表
    @staticmethod
    def get_admin_list(page, size):
        paginator = db.session.query(BaAdmin.id, BaAdmin.username, BaAdmin.nickname, BaAdmin.avatar, BaAdmin.email,
                                     BaAdmin.mobile, BaAdmin.last_login_time, BaAdmin.last_login_ip, BaAdmin.motto,
                                     BaAdmin.status, BaAdmin.update_time, BaAdmin.create_time, BaAdminGroup.id,
                                     BaAdminGroup.name).select_from(BaAdmin) \
            .join(BaAdminGroupAccess, BaAdmin.id == BaAdminGroupAccess.uid) \
            .join(BaAdminGroup, BaAdminGroup.id == BaAdminGroupAccess.group_id) \
            .paginate(page=page, per_page=size, error_out=True)
        return {
            'total': paginator.total,
            'current_page': paginator.page,
            'items': paginator.items
        }

    # 获取加密后的密码
    @staticmethod
    def get_credential(uid):
        credential, = db.session.query(BaAdmin._credential).filter(
            BaAdmin.id == uid,
            BaAdmin.type.in_([
                ClientTypeEnum.USERNAME.value,
                ClientTypeEnum.EMAIL.value,
                ClientTypeEnum.MOBILE.value]),
            BaAdmin._credential != None
        ).first()
        return credential
