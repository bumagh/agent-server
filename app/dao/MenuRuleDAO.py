# -*- coding: utf-8 -*-
from app.model.MenuRuleModel import BaAdminRule


class MeunRuleDAO():

    @staticmethod
    def index():
        results = BaAdminRule.query.all()
        trees = []
        for result in results:
            my_dict = {'id': result.id, 'pid': result.pid, 'type': result.type, 'title': result.title,
                       'name': result.name, 'path': result.path, 'icon': result.icon, 'menu_type': result.menu_type,
                       'url': result.url, 'component': result.component, 'keepalive': result.keepalive,
                       'extend': result.extend, 'remark': result.remark, 'weigh': result.weigh, 'status': result.status,
                       'update_time': result.update_time, 'create_time': result.create_time}
            if result.pid == 0:
                trees.append(my_dict)
            else:
                parent = {}
                for t in trees:
                    if t['id'] == result.pid:
                        parent = t
                if 'children' not in parent:  # 如果没有子节点，创建一个空列表
                    parent['children'] = []
                parent['children'].append(my_dict)
        return {
            'list': trees
        }
