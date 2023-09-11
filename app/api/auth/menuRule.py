# -*- coding: utf-8 -*-
from flask import Blueprint, request

from app.core.error import ParameterException
from app.dao.MenuRuleDAO import MeunRuleDAO
from app.libs.error_code import Success
from app.dao.AdminLogDAO import AdminLogDAO
from app.core.utils import paginate
from app.model.MenuRuleModel import BaAdminRule

menuRule = Blueprint('menuRule', __name__, url_prefix='/auth.Rule')


# 首页查询接口
@menuRule.route("/index", methods=['GET'])
def index():
    tree = MeunRuleDAO.index()
    return Success(tree)


# 获取单条数据接口，用来修改使用
@menuRule.route("/edit", methods=['GET'])
def get_one_obj():
    id = request.args.get("id")
    if id is None:
        raise ParameterException
    data = BaAdminRule.query.get(id)
    data_str = {
        "row": data
    }
    return Success(data_str)


@menuRule.route("/edit", methods=['POST'])
def update_rule():
    id = request.args.get("id", type=int)
    data = BaAdminRule.query.get(id)
    data_str = {
        "row": data
    }
    return Success(data_str)


# 新增接口
@menuRule.route("/add", methods=['POST'])
def add_rule():
    data = request.json()
    extend = data['extend']
    icon = data['icon']
    keepalive = data['keepalive']
    menu_type = data['menu_type']
    name = data['name']
    pid = data['pid']
    remark = data['remark']
    status = data['status']
    title = data['title']
    type = data['type']
    weigh = data['weigh']
    return Success()


# 排序接口,实际上就是对调权重
@menuRule.route("/sortable", methods=['POST'])
def sortable():
    data = request.json()
    id = data['id']
    targetId = data['targetId']
    if id is None or targetId is None:
        raise ParameterException
    origin_rule = BaAdminRule.query.get(id)
    target_rule = BaAdminRule.query.get(targetId)
    # 交换weigh
    origin_rule.update(weigh=target_rule.weigh)
    target_rule.update(weigh=origin_rule.weigh)
    return Success()


# 删除数据接口
# 真删除
@menuRule.route("/del", methods=['DELETE'])
def delete():
    ids = request.args.get("ids[]")
    if ids is None:
        raise ParameterException
    # 将参数转换为整数类型
    ids = [int(id) for id in ids.split(',')]
    print ids
    # 批量删除
    rules = BaAdminRule.query.filter(BaAdminRule.id.in_(ids))
    for rule in rules:
        rule.delete()

    return Success()

# 更新数据接口
