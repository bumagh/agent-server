#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from app.dao.admin_group_access import AdminGroupAccessDao


class AdminService():
    @staticmethod
    def option_group_field(item):
        itmes = list()
        for u in item['items']:
            row_dict = dict(u)
            groupid, groupname = AdminGroupAccessDao.get_user_admin_group_info(row_dict['id'])
            row_dict['groupid'] = groupid
            row_dict['groupname'] = groupname
            itmes.append(row_dict)
        return {
            'total': item['total'],
            'current_page': item['current_page'],
            'items': itmes
        }
