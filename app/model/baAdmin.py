#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sqlalchemy import Column, Integer, String

from app.core.db import EntityModel as Base


class BaAdmin(Base):
    __tablename__ = 'ba_admin'
    id = Column(Integer, primary_key=True)
    username = Column(Integer, nullable=False, comment='用户名')
    nickname = Column(String(60), comment='昵称')
    avatar = Column(String(50), comment='头像')
    email = Column(String(50), comment='邮箱')
    mobile = Column(String(50), comment='手机')
    login_failure = Column(String(50), comment='登录失败次数')
    last_login_time = Column(String(50), comment='上次登录时间')
    last_login_ip = Column(String(50), comment='上次登录IP')
    password = Column(String(50), comment='密码')
    salt = Column(String(50), comment='密码盐')
    motto = Column(String(50), comment='签名')
    status = Column(String(50), comment='状态:0=禁用,1=启用')
    update_time = Column(String(50), comment='更新时间')
    create_time = Column(String(50), comment='创建时间')
