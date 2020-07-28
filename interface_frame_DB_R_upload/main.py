from action.generate_request_data_via_rely import GenerateRequestDataViaRely
from utils.http_client import HttpClient
from action.store_data import *
from action.check_result import *
from utils.log import *


def main():
    # connect DB, get connection instance object [连接DB， 获取连接实例对象 ]
    db = DB()
    # get api list
    api_list = db.get_api_list()
    # No need to deal with index, row 1 is the first group data [第一行就是第一组数据，所以不用处理索引 ]
    for id, api in enumerate(api_list, 1):
        api_id = api[0]
        api_name = api[1]
        request_url = api[2]
        request_method = api[3]
        params_type = api[4]
        info("*********************Case starts*********************")
        info("api info: %s" % [api_id, api_name, request_url, request_method, params_type] )

        # Get test case via api_id [通过 api_id 获取测试用例]
        api_case_list = db.get_certain_api_case(api_id)
        for idx, case in enumerate(api_case_list, 1):
            case_id = case[0]
            # Deal with data type if need, str -> dict
            request_data = eval(case[2]) if case[2] else {}
            debug("request_data is %s and type is %s" % (request_data, type(request_data)))
            request_rely_data = case[3]
            expect_response_code = case[4]
            expect_response_data = eval(case[5]) if case[5] else {}
            data_store_rule = eval(case[7]) if case[7] else {}
            info("case info: %s" % [case_id, request_data, request_rely_data, expect_response_code,
                                    data_store_rule, expect_response_data])

            # If request_rely_data is not empty, generate request data via request_rely_data
            if request_rely_data:
                request_rely_data = eval(request_rely_data)
                request_data = GenerateRequestDataViaRely.gen(request_data, request_rely_data)
                info("api【%s】case %s deals with rely data successfully, request data: %s"
                     % (api_name, idx, request_data))
            else:
                info("api【%s】case %s does not need to deal with rely data" % (api_name, idx))

            # Send request and get response
            hc = HttpClient()
            response = hc.request(request_url, request_method, params_type, request_data)
            # debug("response: %s" % response)
            actual_response_code = response.status_code
            # debug("response_code: %s" % actual_response_code)
            actual_response_body = response.json()
            # debug("actual_response_body: %s" % actual_response_body)
            info("api【%s】case %s actual response message: %s, %s"
                 % (api_name, idx, actual_response_code, actual_response_body))

            # Verify response code
            if actual_response_code == int(expect_response_code):
                # If data_store_rule is not empty, store the needed data (request, response or both )
                # in table: interface_data_store
                if data_store_rule:
                    StoreData.store(data_store_rule, api_name, case_id, request_data, response.json())
                info("api【%s】case %s store data successfully, " % (api_name, idx))
                # Check result and get error_info if fail
                error_info = CheckResult.check(response.json(), expect_response_data)
                info("error info: %s" % error_info)
                if error_info:
                    info("Test result: FAIL. Api【%s】case %s verifies result failed, error message：%s"
                         % (api_name, idx, error_info))
                else:
                    info("Test result: PASS. Api【%s】case %s verifies result successfully" % (api_name, idx))
                info("*********************Case ends*********************\n")
            else:
                info("api【%s】case %s actual response code is %s, not %s"
                      % (api_name, idx, actual_response_code, expect_response_code))


if __name__ == "__main__":
    main()
