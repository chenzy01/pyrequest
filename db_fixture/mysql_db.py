# coding=utf8
import re

import pymysql
from pymysql import connect, cursors
from pymysql.err import OperationalError
import os
from os.path import abspath, dirname
import configparser as cparser

# === 读取 db_config.ini 文件设置 ===
# base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = dirname(dirname(abspath(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")


# ===封装 MYSQL 基本操作===
class DB:
    def __init__(self):
        try:
            # 连接数据库
            self.connection = pymysql.connect(host=host,
                                              port=int(port),
                                              user=user,
                                              password=password,
                                              db=db,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 清除数据
    def clear(self, table_name):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

    # 插入数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ','.join(table_data.keys())
        # '%s' % i for i in
        value = ','.join(table_data.values())
        # list1 = table_data.values()
        # value1 = re.sub("\D", "", list(list1)[0])
        # print(type(list1))
        # value0 = list(list1)
        # print(type(value0[2]))
        # value = '%d' % int(value1) + ',' + ','.join(list('%s' % i for i in table_data.values())[1:])

        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ");"
        print(real_sql)

        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)
        self.connection.commit()

    # 关闭数据库连接
    def close(self):
        self.connection.close()

    # 初始化数据
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':
    db = DB()
    table_name1 = "sign_event"
    data1 = {'id': 12, 'name': '红米', '`limit`': 2000, 'status': 1, 'address': '北京会展中心',
             'start_time': '2016-08-20 00:25:42', 'create_time': '2016-08-20 00:25:42'}
    table_name2 = "sign_guest"
    data2 = {'realname': 'alen', 'phone': 12312341234, 'email': 'alen@mail.com', 'sign': 0,
             'create_time': '2016-08-20 00:25:42', 'event_id': 1}

    db.clear(table_name2)
    db.insert(table_name2, data2)
    db.close()
