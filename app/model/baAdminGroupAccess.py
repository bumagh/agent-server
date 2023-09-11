#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer

from app.core.db import BaseModel as Base


class BaAdminGroupAccess(Base):
    __tablename__ = 'ba_admin_group_access'
    uid = Column(Integer, primary_key=True, nullable=False, comment='管理员ID')
    group_id = Column(Integer, primary_key=True, nullable=False, comment='分组ID')


