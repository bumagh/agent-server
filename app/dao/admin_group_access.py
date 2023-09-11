#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from app.core.db import db
from app.model.baAdminGroup import BaAdminGroup
from app.model.baAdminGroupAccess import BaAdminGroupAccess


class AdminGroupAccessDao():
    @staticmethod
    def get_user_admin_group_info(uid):
        paginator = db.session.query(BaAdminGroup.id, BaAdminGroup.name).select_from(BaAdminGroup) \
            .join(BaAdminGroupAccess, BaAdminGroup.id == BaAdminGroupAccess.group_id) \
            .filter_by(uid=uid).all()
        return [(u.id) for u in paginator], [(u.name) for u in paginator]
