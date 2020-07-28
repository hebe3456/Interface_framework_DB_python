import os


# abs path of project
baseDir = os.path.dirname(os.path.dirname(__file__))

# db config file abs path
config_path = baseDir + "/config/db_config.ini"

# logger config file abs path
log_file_path = baseDir + "/config/Logger.conf"


if __name__ == "__main__":
    print(log_file_path)
