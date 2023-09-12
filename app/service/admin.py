#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from app.dao.admin_group_access import AdminGroupAccessDao


class AdminService():
    @staticmethod
    def option_group_field(item):
        itmes = list()
        for u in item.items:
            row_dict = dict(u)
            groupid, groupname = AdminGroupAccessDao.get_user_admin_group_info(row_dict['id'])
            row_dict['group_arr'] = groupid
            row_dict['group_name_arr'] = groupname
            itmes.append(row_dict)
        return {
            'total': item.total,
            'remark': "",
            'list': itmes
        }
