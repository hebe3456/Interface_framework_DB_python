from utils.md5_encrypt import md5_encrypt
from utils.db_handler import DB


class GenerateRequestDataViaRely(object):
    def __init__(self):
        pass

    @classmethod
    def gen(cls, data_source, request_rely_data, header={}):
        """
        :param data_source:
        :param request_rely_data: case 表里的 request_rely_data字段 的值
        :param header:
        :return:
        """
        # deep copy，so that don't change data_source
        data_source_copy = data_source.copy()
        db = DB()
        for key, value in request_rely_data.items():
            for k, v in value.items():
                # 取出依赖数据的 api_name, case_id
                api_name, case_id = k.split("->")
                api_id = db.get_api_id(api_name)
                store_rely_data = db.get_rely_data(api_id, int(case_id))

                for i in v:
                    if key == "request":
                        if i in store_rely_data["request"][api_name][int(case_id)]:    # int or str
                            if i == "password":
                                # md5 encrypt
                                password = md5_encrypt(store_rely_data["request"][api_name][int(case_id)][i])
                                data_source_copy[i] = password
                            else:
                                data_source_copy[i] = store_rely_data["request"][api_name][int(case_id)][i]     # 不该原始数据，改data
                    elif key == "response":
                        if i in store_rely_data["response"][api_name][int(case_id)]:
                            data_source_copy[i] = store_rely_data["response"][api_name][int(case_id)][i]

        return data_source_copy


if __name__ == "__main__":
    data_source = {}
    request_rely_data = {}
    print(GenerateRequestDataViaRely.gen(data_source, request_rely_data))
