# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Enum, String
from app.core.db import BaseModel as Base


class BaAdminRule(Base):
    __tablename__ = 'ba_admin_rule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=False, comment='上级菜单')
    type = Column(Enum('menu_dir', 'menu', 'button'), nullable=False,
                  comment='类型:menu_dir=菜单目录,menu=菜单项,button=页面按钮')
    title = Column(String(50), nullable=False, comment='标题')
    name = Column(String(50), nullable=False, comment='规则名称')
    path = Column(String(100), nullable=False, comment='路由路径')
    icon = Column(String(50), nullable=False, comment='图标')
    menu_type = Column(Enum('tab', 'link', 'iframe'), nullable=False,
                       comment='菜单类型:tab=选项卡,link=链接,iframe=Iframe')
    url = Column(String(255), default=' ', nullable=False, comment='Url')
    component = Column(String(100), nullable=False, comment='组件路径')
    keepalive = Column(Integer, nullable=False, comment='缓存:0=关闭,1=开启')
    extend = Column(Enum('none', 'add_rules_only', 'add_menu_only'), nullable=False,
                    comment='扩展属性:none=无,add_rules_only=只添加为路由,add_menu_only=只添加为菜单')
    remark = Column(String(255), nullable=False, comment='备注')
    weigh = Column(Integer, nullable=False, comment='权重')
    status = Column(Enum('0', '1'), nullable=False, comment='状态:0=禁用,1=启用')
