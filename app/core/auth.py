# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/3/24.
  权限相关的变量与方法
"""
from flask import current_app
from werkzeug.local import LocalProxy
from app.core.error import NotFound
from flasgger import Swagger

ep_meta = LocalProxy(lambda: get_ep_meta())

def find_info_by_ep(ep):
    '''通过请求的endpoint寻找路由函数的meta信息'''
    _ep_meta = current_app.config['EP_META']
    return _ep_meta.get(ep)

def get_ep_meta():
    _ep_meta = current_app.config['EP_META']
    return _ep_meta if _ep_meta else {}


def find_auth_module(name):
    '''通过权限寻找meta信息
    :param name: '新增商品'
    :return: meta(name='新增商品', module='商品')
    '''
    for _, meta in ep_meta.items():
        if meta.name == name:
            return meta
    return None


def get_ep_name(id):
    '''根据id查询对应的endpoint_info，返回endpoint的name(中文)
    :param id: endpoint_info的id(id每次都是自动生成的)
    :return:
    '''
    ep_info_list = current_app.config['EP_INFO_LIST']
    ep_name = None
    for ep_info in ep_info_list:
        if ep_info['id'] == id:
            ep_name = ep_info['name']
    if not ep_name:
        raise NotFound(msg='权限ID:{} 不存在'.format(id))
    return ep_name


def get_ep_id(name):
    '''根据name查询对应的endpoint_info，返回endpoint的id
    :param name:
    :return:
    '''
    ep_info_list = current_app.config['EP_INFO_LIST']
    ep_id = None
    for ep_info in ep_info_list:
        if ep_info['name'] == name:
            ep_id = ep_info['id']
    if not ep_id:
        raise NotFound(msg='权限名:{} 不存在'.format(name))
    return ep_id
