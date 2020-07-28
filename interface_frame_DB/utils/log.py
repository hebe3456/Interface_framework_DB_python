import logging.config     # 读取配置文件

from config.public_data import log_file_path


# 读取日志配置文件
logging.config.fileConfig(log_file_path)
# 选择一个日志格式
logger = logging.getLogger("example02")     # 或者example01


def debug(message):
    # 定义debug级别日志打印方法
    logger.debug(message)


def info(message):
    # 定义info级别日志打印方法
    logger.info(message)


def warning(message):
    # 定义warning级别日志打印方法
    logger.warning(message)


def error(message):
    # 定义warning级别日志打印方法
    logger.error(message)


if __name__ == "__main__":
    warning("aaa")