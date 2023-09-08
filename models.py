from sqlacodegen.codegen import Model
from sqlalchemy import Column, String, Integer, Enum, Text

class BaAdmin(Model):
    __tablename__ = 'ba_admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20),nullable=False,unique=True,comment='ID')
    nickname = Column(String(50),nullable=False,comment='用户名')
    avatar = Column(String(255),nullable=False,comment='昵称')
    email = Column(String(50),nullable=False,comment='头像')
    mobile = Column(String(11),nullable=False,comment='邮箱')
    login_failure = Column(Integer,nullable=False,comment='手机')
    last_login_time = Column(Integer,nullable=False,comment='登录失败次数')
    last_login_ip = Column(String(50),nullable=False,comment='上次登录时间')
    password = Column(String(32),nullable=False,comment='上次登录IP')
    salt = Column(String(30),nullable=False,comment='密码')
    motto = Column(String(255),nullable=False,comment='密码盐')
    status = Column(Enum('0','1'),nullable=False,comment='签名')
    update_time = Column(Integer,nullable=False,comment='状态:0=禁用,1=启用')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaAdminGroup(Model):
    __tablename__ = 'ba_admin_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer,nullable=False,comment='ID')
    name = Column(String(100),nullable=False,comment='上级分组')
    rules = Column(Text,nullable=False,comment='组名')
    status = Column(Enum('0','1'),nullable=False,comment='权限规则ID')
    update_time = Column(Integer,nullable=False,comment='状态:0=禁用,1=启用')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaAdminGroupAccess(Model):
    __tablename__ = 'ba_admin_group_access'
    group_id = Column(Integer,nullable=False,comment='管理员ID')

class BaAdminLog(Model):
    __tablename__ = 'ba_admin_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer,nullable=False,comment='ID')
    username = Column(String(20),nullable=False,comment='管理员ID')
    url = Column(String(1500),nullable=False,comment='管理员用户名')
    title = Column(String(100),nullable=False,comment='操作Url')
    data = Column(Text,nullable=False,comment='日志标题')
    ip = Column(String(50),nullable=False,comment='请求数据')
    useragent = Column(String(255),nullable=False,comment='IP')
    create_time = Column(Integer,nullable=False,comment='User-Agent')

class BaAdminRule(Model):
    __tablename__ = 'ba_admin_rule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer,nullable=False,comment='ID')
    type = Column(Enum('menu_dir','menu','button'),nullable=False,comment='上级菜单')
    title = Column(String(50),nullable=False,comment='类型:menu_dir=菜单目录,menu=菜单项,button=页面按钮')
    name = Column(String(50),nullable=False,comment='标题')
    path = Column(String(100),nullable=False,comment='规则名称')
    icon = Column(String(50),nullable=False,comment='路由路径')
    menu_type = Column(Enum('tab','link','iframe'),nullable=False,comment='图标')
    url = Column(String(255),nullable=False,comment='菜单类型:tab=选项卡,link=链接,iframe=Iframe')
    component = Column(String(100),nullable=False,comment='Url')
    keepalive = Column(Integer,nullable=False,comment='组件路径')
    extend = Column(Enum('none','add_rules_only','add_menu_only'),nullable=False,comment='缓存:0=关闭,1=开启')
    remark = Column(String(255),nullable=False,comment='扩展属性:none=无,add_rules_only=只添加为路由,add_menu_only=只添加为菜单')
    weigh = Column(Integer,nullable=False,comment='备注')
    status = Column(Enum('0','1'),nullable=False,comment='权重')
    update_time = Column(Integer,nullable=False,comment='状态:0=禁用,1=启用')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaArea(Model):
    __tablename__ = 'ba_area'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer,nullable=False,comment='ID')
    shortname = Column(String(100),nullable=False,comment='父id')
    name = Column(String(100),nullable=False,comment='简称')
    mergename = Column(String(255),nullable=False,comment='名称')
    level = Column(Integer,nullable=False,comment='全称')
    pinyin = Column(String(100),nullable=False,comment='层级:1=省,2=市,3=区/县')
    code = Column(String(100),nullable=False,comment='拼音')
    zip = Column(String(100),nullable=False,comment='长途区号')
    first = Column(String(50),nullable=False,comment='邮编')
    lng = Column(String(50),nullable=False,comment='首字母')
    lat = Column(String(50),nullable=False,comment='经度')

class BaAttachment(Model):
    __tablename__ = 'ba_attachment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(20),nullable=False,comment='ID')
    admin_id = Column(Integer,nullable=False,comment='细目')
    user_id = Column(Integer,nullable=False,comment='上传管理员ID')
    url = Column(String(255),nullable=False,comment='上传用户ID')
    width = Column(Integer,nullable=False,comment='物理路径')
    height = Column(Integer,nullable=False,comment='宽度')
    name = Column(String(100),nullable=False,comment='高度')
    size = Column(Integer,nullable=False,comment='原始名称')
    mimetype = Column(String(100),nullable=False,comment='大小')
    quote = Column(Integer,nullable=False,comment='mime类型')
    storage = Column(String(50),nullable=False,comment='上传(引用)次数')
    sha1 = Column(String(40),nullable=False,comment='存储方式')
    create_time = Column(Integer,nullable=False,comment='sha1编码')
    last_upload_time = Column(Integer,nullable=False,comment='创建时间')

class BaCaptcha(Model):
    __tablename__ = 'ba_captcha'
    code = Column(String(32),nullable=False,comment='验证码Key')
    captcha = Column(Text,nullable=False,comment='验证码(加密后)')
    create_time = Column(Integer,nullable=False,comment='验证码数据')
    expire_time = Column(Integer,nullable=False,comment='创建时间')

class BaConfig(Model):
    __tablename__ = 'ba_config'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30),nullable=False,unique=True,comment='ID')
    group = Column(String(30),nullable=False,comment='变量名')
    title = Column(String(50),nullable=False,comment='分组')
    tip = Column(String(100),nullable=False,comment='变量标题')
    type = Column(String(30),nullable=False,comment='变量描述')
    value = Column(Text,nullable=False,comment='变量输入组件类型')
    content = Column(Text,nullable=False,comment='变量值')
    rule = Column(String(100),nullable=False,comment='字典数据')
    extend = Column(String(255),nullable=False,comment='验证规则')
    allow_del = Column(Integer,nullable=False,comment='扩展属性')
    weigh = Column(Integer,nullable=False,comment='允许删除:0=否,1=是')

class BaCrudLog(Model):
    __tablename__ = 'ba_crud_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(200),nullable=False,comment='ID')
    table = Column(Text,nullable=False,comment='数据表名')
    fields = Column(Text,nullable=False,comment='数据表数据')
    status = Column(Enum('delete','success','error','start'),nullable=False,comment='字段数据')
    create_time = Column(Integer,nullable=False,comment='状态:delete=已删除,success=成功,error=失败,start=生成中')

class BaMigrations(Model):
    __tablename__ = 'ba_migrations'
    migration_name = Column(String(100),nullable=False,comment='')
    start_time = Column(nullable=False,comment='')
    end_time = Column(nullable=False,comment='')
    breakpoint = Column(Integer,nullable=False,comment='')

class BaSecurityDataRecycle(Model):
    __tablename__ = 'ba_security_data_recycle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50),nullable=False,comment='ID')
    controller = Column(String(100),nullable=False,comment='规则名称')
    controller_as = Column(String(100),nullable=False,comment='控制器')
    data_table = Column(String(100),nullable=False,comment='控制器别名')
    primary_key = Column(String(50),nullable=False,comment='对应数据表')
    status = Column(Enum('0','1'),nullable=False,comment='数据表主键')
    update_time = Column(Integer,nullable=False,comment='状态:0=禁用,1=启用')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaSecurityDataRecycleLog(Model):
    __tablename__ = 'ba_security_data_recycle_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer,nullable=False,comment='ID')
    recycle_id = Column(Integer,nullable=False,comment='操作管理员')
    data = Column(Text,nullable=False,comment='回收规则ID')
    data_table = Column(String(100),nullable=False,comment='回收的数据')
    primary_key = Column(String(50),nullable=False,comment='数据表')
    is_restore = Column(Integer,nullable=False,comment='数据表主键')
    ip = Column(String(50),nullable=False,comment='是否已还原:0=否,1=是')
    useragent = Column(String(255),nullable=False,comment='操作者IP')
    create_time = Column(Integer,nullable=False,comment='User-Agent')

class BaSecuritySensitiveData(Model):
    __tablename__ = 'ba_security_sensitive_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50),nullable=False,comment='ID')
    controller = Column(String(100),nullable=False,comment='规则名称')
    controller_as = Column(String(100),nullable=False,comment='控制器')
    data_table = Column(String(100),nullable=False,comment='控制器别名')
    primary_key = Column(String(50),nullable=False,comment='对应数据表')
    data_fields = Column(Text,nullable=False,comment='数据表主键')
    status = Column(Enum('0','1'),nullable=False,comment='敏感数据字段')
    update_time = Column(Integer,nullable=False,comment='状态:0=禁用,1=启用')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaSecuritySensitiveDataLog(Model):
    __tablename__ = 'ba_security_sensitive_data_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer,nullable=False,comment='ID')
    sensitive_id = Column(Integer,nullable=False,comment='操作管理员')
    data_table = Column(String(100),nullable=False,comment='敏感数据规则ID')
    primary_key = Column(String(50),nullable=False,comment='数据表')
    data_field = Column(String(50),nullable=False,comment='数据表主键')
    data_comment = Column(String(50),nullable=False,comment='被修改字段')
    id_value = Column(Integer,nullable=False,comment='被修改项')
    before = Column(Text,nullable=False,comment='被修改项主键值')
    after = Column(Text,nullable=False,comment='修改前')
    ip = Column(String(50),nullable=False,comment='修改后')
    useragent = Column(String(255),nullable=False,comment='操作者IP')
    is_rollback = Column(Integer,nullable=False,comment='User-Agent')
    create_time = Column(Integer,nullable=False,comment='是否已回滚:0=否,1=是')

class BaTestBuild(Model):
    __tablename__ = 'ba_test_build'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100),nullable=False,comment='ID')
    keyword_rows = Column(String(100),nullable=False,comment='标题')
    content = Column(Text,nullable=False,comment='关键词')
    views = Column(Integer,nullable=False,comment='内容')
    likes = Column(Integer,nullable=False,comment='浏览量')
    dislikes = Column(Integer,nullable=False,comment='有帮助数')
    note_textarea = Column(String(100),nullable=False,comment='无帮助数')
    status = Column(Enum('0','1'),nullable=False,comment='备注')
    weigh = Column(Integer,nullable=False,comment='状态:0=隐藏,1=正常')
    update_time = Column(Integer,nullable=False,comment='权重')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaToken(Model):
    __tablename__ = 'ba_token'
    type = Column(String(15),nullable=False,comment='Token')
    user_id = Column(Integer,nullable=False,comment='类型')
    create_time = Column(Integer,nullable=False,comment='用户ID')
    expire_time = Column(Integer,nullable=False,comment='创建时间')

class BaUser(Model):
    __tablename__ = 'ba_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer,nullable=False,comment='ID')
    username = Column(String(32),nullable=False,unique=True,comment='分组ID')
    nickname = Column(String(50),nullable=False,comment='用户名')
    email = Column(String(50),nullable=False,comment='昵称')
    mobile = Column(String(11),nullable=False,comment='邮箱')
    avatar = Column(String(255),nullable=False,comment='手机')
    gender = Column(Integer,nullable=False,comment='头像')
    birthday = Column(nullable=False,comment='性别:0=未知,1=男,2=女')
    money = Column(Integer,nullable=False,comment='生日')
    score = Column(Integer,nullable=False,comment='余额')
    last_login_time = Column(Integer,nullable=False,comment='积分')
    last_login_ip = Column(String(50),nullable=False,comment='上次登录时间')
    login_failure = Column(Integer,nullable=False,comment='上次登录IP')
    join_ip = Column(String(50),nullable=False,comment='登录失败次数')
    join_time = Column(Integer,nullable=False,comment='加入IP')
    motto = Column(String(255),nullable=False,comment='加入时间')
    password = Column(String(32),nullable=False,comment='签名')
    salt = Column(String(30),nullable=False,comment='密码')
    status = Column(String(30),nullable=False,comment='密码盐')
    update_time = Column(Integer,nullable=False,comment='状态')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaUserGroup(Model):
    __tablename__ = 'ba_user_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50),nullable=False,comment='ID')
    rules = Column(Text,nullable=False,comment='组名')
    status = Column(Enum('0','1'),nullable=False,comment='权限节点')
    update_time = Column(Integer,nullable=False,comment='状态:0=禁用,1=启用')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaUserMoneyLog(Model):
    __tablename__ = 'ba_user_money_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,nullable=False,comment='ID')
    money = Column(Integer,nullable=False,comment='会员ID')
    before = Column(Integer,nullable=False,comment='变更余额')
    after = Column(Integer,nullable=False,comment='变更前余额')
    memo = Column(String(255),nullable=False,comment='变更后余额')
    create_time = Column(Integer,nullable=False,comment='备注')

class BaUserRule(Model):
    __tablename__ = 'ba_user_rule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer,nullable=False,comment='ID')
    type = Column(Enum('route','menu_dir','menu','nav_user_menu','nav','button'),nullable=False,comment='上级菜单')
    title = Column(String(50),nullable=False,comment='类型:route=路由,menu_dir=菜单目录,menu=菜单项,nav_user_menu=顶栏会员菜单下拉项,nav=顶栏菜单项,button=页面按钮')
    name = Column(String(50),nullable=False,comment='标题')
    path = Column(String(100),nullable=False,comment='规则名称')
    icon = Column(String(50),nullable=False,comment='路由路径')
    menu_type = Column(Enum('tab','link','iframe'),nullable=False,comment='图标')
    url = Column(String(255),nullable=False,comment='菜单类型:tab=选项卡,link=链接,iframe=Iframe')
    component = Column(String(100),nullable=False,comment='Url')
    no_login_valid = Column(Integer,nullable=False,comment='组件路径')
    extend = Column(Enum('none','add_rules_only','add_menu_only'),nullable=False,comment='未登录有效:0=否,1=是')
    remark = Column(String(255),nullable=False,comment='扩展属性:none=无,add_rules_only=只添加为路由,add_menu_only=只添加为菜单')
    weigh = Column(Integer,nullable=False,comment='备注')
    status = Column(Enum('0','1'),nullable=False,comment='权重')
    update_time = Column(Integer,nullable=False,comment='状态:0=禁用,1=启用')
    create_time = Column(Integer,nullable=False,comment='更新时间')

class BaUserScoreLog(Model):
    __tablename__ = 'ba_user_score_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,nullable=False,comment='ID')
    score = Column(Integer,nullable=False,comment='会员ID')
    before = Column(Integer,nullable=False,comment='变更积分')
    after = Column(Integer,nullable=False,comment='变更前积分')
    memo = Column(String(255),nullable=False,comment='变更后积分')
    create_time = Column(Integer,nullable=False,comment='备注')

