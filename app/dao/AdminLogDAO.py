# -*- coding: utf-8 -*-
from app.model.AdminLogModel import AdminLog


class AdminLogDAO():

    @staticmethod
    def queryByPage(page,size):
        logs = AdminLog.query.paginate(page=page, per_page=size, error_out=True)
        return {
            'total': logs.total,
            'list': logs.items
        }
