from configparser import ConfigParser
from config.public_data import config_path


class ConfigParse(object):
    def __init__(self):
        pass

    @classmethod
    def get_db_config(cls):
        # 创建解析配置文件的实例对象，用configparser包，记得安装
        cls.cf = ConfigParser()
        #  用read方法都文件配置
        cls.cf.read(config_path)
        host = cls.cf.get("mysqlconf", "host")
        port = cls.cf.get("mysqlconf", "port")
        user = cls.cf.get("mysqlconf", "user")
        password = cls.cf.get("mysqlconf", "password")
        db = cls.cf.get("mysqlconf", "db_name")
        return {"host": host, "port": port, "user": user, "password": password, "db": db}


if __name__ == "__main__":
    print(ConfigParse.get_db_config())    # 类名调用类方法
    # cp = ConfigParse()
    # print(cp.get_db_config())