# -*- coding: utf-8 -*-
from app.model.AdminLogModel import AdminLog


class AdminLogDAO():

    @staticmethod
    def queryByPage(page, size, quickSearch):
        logs = {}
        if quickSearch is None:
            logs = AdminLog.query.paginate(page=page, per_page=size, error_out=True)
        else:
            logs = AdminLog.query.filter(AdminLog.title.like(u'%{}%'.format(quickSearch))).paginate(page=page, per_page=size, error_out=True)
        return {
            'total': logs.total,
            'list': logs.items
        }
