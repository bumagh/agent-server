#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from sqlalchemy import Column, Integer, String, Enum, func

from app.core.db import EntityModel as Base
from app.core.utils import generate_random_salt


class BaAdmin(Base):
    __tablename__ = 'ba_admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False, unique=True, comment='用户名')
    nickname = Column(String(50), nullable=False, comment='昵称')
    avatar = Column(String(255), nullable=False, comment='头像')
    email = Column(String(50), nullable=False, comment='邮箱')
    mobile = Column(String(11), nullable=False, comment='手机')
    login_failure = Column(Integer, nullable=False, comment='登录失败次数')
    last_login_time = Column(Integer, nullable=False, comment='上次登录时间')
    last_login_ip = Column(String(50), nullable=False, comment='上次登录IP')
    password = Column(String(32), nullable=False, comment='密码')
    salt = Column(String(30), nullable=False, comment='密码盐')
    motto = Column(String(255), nullable=False, comment='签名')
    status = Column(Enum('0', '1'), nullable=False, comment='状态:0=禁用,1=启用')

    def __init__(self, *args, **kwargs):
        super(BaAdmin, self).__init__(*args, **kwargs)
        self.initialize()

    def initialize(self):
        if self.salt is None:
            self.salt = generate_random_salt()
        if self.login_failure is None:
            self.login_failure = 0
        if self.last_login_ip is None:
            self.last_login_ip = '127.0.0.1'
        if self.motto is None:
            self.motto = ''
