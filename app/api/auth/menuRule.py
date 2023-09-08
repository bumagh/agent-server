# -*- coding: utf-8 -*-
from flask import Blueprint

from app.dao.MenuRuleDAO import MeunRuleDAO
from app.libs.error_code import Success
from app.dao.AdminLogDAO import AdminLogDAO
from app.core.utils import paginate

menuRule = Blueprint('menuRule', __name__, url_prefix='/auth.Rule')


@menuRule.route("/index", methods=['GET'])
def index():
    tree = MeunRuleDAO.index()
    return Success(tree)
