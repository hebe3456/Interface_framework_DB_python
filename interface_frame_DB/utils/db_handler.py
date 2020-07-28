import pymysql
from datetime import datetime

from utils.config_handler import ConfigParse
from utils.log import *


class DB(object):
    def __init__(self):
        # 连接DB
        # 调用ConfigParse类的类方法get_db_config，获得配置信息
        self.db_conf = ConfigParse.get_db_config()
        # 获取DB连接实例对象
        self.conn = pymysql.connect(
            host=self.db_conf["host"],
            port=int(self.db_conf["port"]),
            user=self.db_conf["user"],
            password=self.db_conf["password"],
            database=self.db_conf["db"],
            charset="utf8"
        )
        # 获取DB游标实例对象
        self.cur = self.conn.cursor()

    def close_connect(self):
        # 关闭数据连接
        # 提交
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭DB连接
        self.conn.close()

    def get_api_list(self):
        # 获取需要执行（status=1）的所有api信息
        sql_str = "select * from interface_api where status=1"
        # 游标execute方法，执行sql语句
        self.cur.execute(sql_str)
        # 得到元组对象
        data = self.cur.fetchall()
        # 转成数组
        api_list = list(data)
        return api_list

    def get_certain_api_case(self, api_id):
        # 获取某一api需要执行（status=1）的所有case信息
        sql_str = "select * from interface_test_case where api_id=%s and status=1" % api_id
        self.cur.execute(sql_str)
        api_case_list = list(self.cur.fetchall())
        return api_case_list

    def get_rely_data(self, api_id, case_id):
        # 获取表 interface_data_store 的 data_store 字段值
        sql_str = "select data_store from interface_data_store where api_id=%s and case_id=%s" % (api_id, case_id)
        self.cur.execute(sql_str)
        # info(self.cur.fetchall()[0][0])        调式，看数据格式，
        date_store_str = self.cur.fetchall()[0][0]
        # 判断值存在且为字符串格式
        if date_store_str and isinstance(date_store_str, str):
            try:
                rely_data = eval(date_store_str)
                return rely_data
            except Exception as e:
                info("获取接口【%s】用例【%s】存储的依赖数据格式有误，请确认" % (api_id, case_id))
                info(e)
        else:
            info("获取接口【%s】用例【%s】存储的依赖数据失败，请确认" % (api_id, case_id))

    def write_check_result(self, case_id, error_info, response_data):
        sql_str = "update interface_test_case set error_info=\"%s\", res_data=\"%s\" where id=%s" \
                  % (error_info, response_data, case_id)
        self.cur.execute(sql_str)
        self.conn.commit()

    def get_api_id(self, api_name):
        # 因为api_name 是唯一的
        sql_str = "select api_id from interface_api where api_name='%s'" % api_name
        self.cur.execute(sql_str)
        # 查看方法，看怎么去用，不熟悉的时候
        # print(dir(self.cur))
        # print(help(self.cur.fetchall))
        # api_id = self.cur.fetchall()      # ((1,),)
        api_id = self.cur.fetchall()[0][0]
        return api_id

    def update_store_data(self, api_id, case_id, data_store):
        # 先查找数据，存在就修改，不存在就添加
        sql_str = "select data_store from interface_data_store where api_id = %s and case_id = %s" % (api_id, case_id)
        self.cur.execute(sql_str)
        if self.cur.fetchall():
            sql_str = "update interface_data_store set data_store = \"%s\" where api_id = %s and case_id = %s" \
                      % (data_store, api_id, case_id)
            print(sql_str)
            self.cur.execute(sql_str)
            self.conn.commit()
        else:
            sql_str = "insert into interface_data_store values (%s, %s, \"%s\", '%s')" % (api_id, case_id, data_store, datetime.now())
            print(sql_str)
            self.cur.execute(sql_str)
            self.conn.commit()


if __name__ == "__main__":
    db = DB()
    # print(db.get_api_list())
    # print(db.get_certain_api_case(1))
    # print(db.get_certain_api_case(2))
    # DB中格式为'{}'、 str:'test'，分别测试
    print(db.get_rely_data(1, 1))
    # print(db.get_rely_data(1, 2))

    # api_list = db.get_api_list()
    # print(api_list[0][0])

    print(db.get_api_id("用户注册"))
    db.update_store_data(1, 3, "{}")

# 注：
# 取出的数据可能是None 或 空字符串 ‘’




