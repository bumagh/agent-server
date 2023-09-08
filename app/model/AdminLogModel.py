# -*- coding: utf-8 -*-
from app import db

class AdminLog(db.Model):
    __tablename__ = 'ba_admin_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, nullable=False, comment='ID')
    username = Column(String(20), nullable=False, comment='管理员ID')
    url = Column(String(1500), nullable=False, comment='管理员用户名')
    title = Column(String(100), nullable=False, comment='操作Url')
    data = Column(Text, nullable=False, comment='日志标题')
    ip = Column(String(50), nullable=False, comment='请求数据')
    useragent = Column(String(255), nullable=False, comment='IP')
    create_time = Column(Integer, nullable=False, comment='User-Agent')
