from utils.db_handler import DB
from utils.log import *


class StoreData(object):
    def __init__(self):
        pass

    @classmethod
    def store(cls, store_data_rule, api_name, case_id, request_source={}, response_source={}):
        store_data = {"request": {}, "response": {}}

        for key, value in store_data_rule.items():
            if key == "request":
                # get data from request body
                for i in value:
                    if i in request_source:
                        val = request_source[i]
                        if api_name not in store_data["request"]:
                            store_data["request"] = {api_name: {case_id: {i: val}}}
                        elif case_id not in store_data["request"][api_name]:
                            store_data["request"][api_name] = {case_id: {i: val}}
                        else:
                            store_data["request"][api_name][case_id][i] = val
                    else:
                        print("Filed %s does not in request_source" % i)

            elif key == "response":
                # get data from response body
                for i in value:
                    if i in response_source:
                        val = response_source[i]
                        if api_name not in store_data["response"]:
                            store_data["response"] = {api_name: {case_id: {i: val}}}
                        elif case_id not in store_data["response"][api_name]:
                            store_data["response"][api_name] = {case_id: {i: val}}
                        else:
                            store_data["response"][api_name][case_id][i] = val
                    else:
                        print("Filed %s does not in response_source" % i)
        info("store_data: %s" % store_data)

        if store_data["request"] or store_data["response"]:
            db = DB()
            api_id = db.get_api_id(api_name)
            db.update_store_data(api_id, int(case_id), store_data)


if __name__ == "__main__":
    store_data_rule1 = {}
    req_source = {}
    res_source = {}
    # StoreData.store(store_point, "用户注册", 1, req_source, res_source)
    StoreData.store(store_data_rule1, "用户注册", 2, req_source, res_source)
