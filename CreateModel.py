# -*- coding: utf-8 -*-
import string

from flask_sqlalchemy import SQLAlchemy
import pymysql
import re
import os

USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = 3306
DATABASE = 'build_admin'


# 创建数据库连接
def create_connection(host, user, password, db):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db
    )
    return connection


# 创建model类
def create_model(table_name, connection):
    model = ""
    model += "class {0}(Model):\n".format(table_name.title().replace("_", ""))
    cursor = connection.cursor()
    cursor.execute("DESCRIBE `{}`".format(table_name))
    columns = cursor.fetchall()
    model += "    __tablename__ = '{}'\n".format(table_name)
    # Add primary key and auto_increment

    if columns[0][0] == "id":
        model += "    id = Column(Integer, primary_key=True, autoincrement=True)\n"

    cursor.execute("SHOW FULL COLUMNS FROM `{}`".format(table_name))
    full_columns = cursor.fetchall()
    for index, col in enumerate(columns[1:]):
        # attr = col[0].replace("_", " ").title() 处理字段名
        str = '    '
        str += col[0]
        str += ' = Column('
        if col[1].startswith('int') or col[1].startswith('bigint') or col[1].startswith('tinyint'):
            str += 'Integer,'
        elif col[1].startswith('varchar'):
            match = re.search('\((\w+)\)', col[1])
            str += 'String({}),'.format(match.group(1))
        elif col[1].startswith('text') or col[1].startswith('longtext'):
            str += 'Text,'
        elif col[1].startswith('enum'):
            str += col[1].replace('enum', 'Enum')
            str += ','
        if col[2]:
            str += 'nullable=False,'

        if col[3] == 'UNI':
            str += 'unique=True,'

        str += "comment='{}',".format(full_columns[index+1][8])

        str = str[:-1]
        str += ')\n'
        model += str
    model += "\n"
    return model


# 主程序
if __name__ == "__main__":
    # 连接到数据库
    connection = create_connection(HOST, USERNAME, PASSWORD, DATABASE)
    # 确保连接被关闭
    # os.system('echo "%s" > db.txt' % connection.get_dsn())
    # 创建Flask SQLAlchemy对象
    db = SQLAlchemy()
    # 获取所有表名
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()  # return a list of tuples
    # 为每个表创建model类并写入文件
    with open('models.py', 'w') as f:
        f.write('from sqlacodegen.codegen import Model\n' +
                'from sqlalchemy import Column, String, Integer, Enum, Text\n\n')
        for table in tables:
            table_name = table[0]  # table name is the first item in the tuple
            f.write(create_model(table_name, connection))
