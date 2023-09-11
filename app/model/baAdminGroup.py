#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer, String, Text, Enum

from app.core.db import BaseModel as Base


class BaAdminGroup(Base):
    __tablename__ = 'ba_admin_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=False, comment='上级分组')
    name = Column(String(100), nullable=False, comment='组名')
    rules = Column(Text, nullable=False, comment='权限规则ID')
    status = Column(Enum('0', '1'), nullable=False, comment='状态:0=禁用,1=启用')
    update_time = Column(Integer, nullable=False, comment='更新时间')
    create_time = Column(Integer, nullable=False, comment='创建时间')
