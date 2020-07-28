import requests
import json

from utils.log import *
# send request and get response


class HttpClient(object):
    def __init__(self):
        pass

    def request(self, request_url, request_method, params_type, request_body, headers=None, cookies=None):
        # handle http request, support both get and post method now, be extensible
        # cannot use requests, since it is keyword -- error
        # request_body should be dict type, if not, deal with it first
        if isinstance(request_body, str):
            request_body = eval(request_body)
        if request_method.lower() == "post":        # 兼容大小写
            # request_method is post, need to use json.dumps() to deal with it first
            if params_type.lower() == "data":
                # the type of request_body is data, form submission
                response = self.__post(request_url, data=json.dumps(request_body), headers=headers, cookies=cookies)
            elif params_type.lower() == "json":
                # the type of request_body is json
                # debug(type(request_data))                   # DEBUG <class 'dict'>
                # debug(type(json.dumps(request_data)))       # DEBUG <class 'str'>
                # if json，type：dict，no need to json.dumps()
                response = self.__post(request_url, json=request_body, headers=headers, cookies=cookies)

        elif request_method.lower() == "get":
            # request_method is get
            if params_type == "url":
                # concat url with request_body
                request_url = "%s%s" % (request_url, request_body)
                response = requests.__get(request_url, headers=headers, cookies=cookies)
            elif params_type == "params":
                response = requests.__get(request_url, request_body, headers=headers, cookies=cookies)
        # Be extensible可扩展，support other request method，such as：delete、put、head、option、trace
        elif request_method.lower() == "put":
            pass
        return response

    def __post(self, url, data=None, json=None, **kwargs):
        # 设置私有方法，处理post各种情况的请求，安全，外部不能随意修改或调用
        response = requests.post(url, data=data, json=json, **kwargs)   # 综合处理含只data、只含json或二者都含有的情况
        return response

    def __get(self, url, params=None, **kwargs):
        # 处理get类各种情况的请求
        response = requests.get(url, params=params, **kwargs)
        return response


if __name__ == "__main__":
    hc = HttpClient()
    # 编码规范：res，不要和类里的response一样
    url = ""
    request_body_data = {}
    res = hc.request(url, "post", "form", request_body_data)
    info(res.status_code)
    info(res.json())

    url = ""
    request_body_data = {}
    res = hc.request(url, "post", "json", request_body_data)
    info(res.status_code)
    info(res.json())

