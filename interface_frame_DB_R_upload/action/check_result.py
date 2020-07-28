import re


class CheckResult(object):
    def __init__(self):
        pass

    @classmethod
    def check(cls, response_obj, check_point):
        """
        可能用到response_obj 中的很多内容
        :param response_obj:
        :param check_point: 
        :return: 
        """
        error_info_dict = {}
        for key, value in check_point.items():
            # source_data = response_obj[key]
            # 需要对key做判空处理
            source_data = response_obj[key] if key in response_obj else ""

            if isinstance(value, str):
                # 等值校验
                if key in response_obj:
                    if not source_data == value:
                        error_info_dict[key] = source_data
                else:
                    error_info_dict[key] = "not exist"

            elif isinstance(value, dict):
                # 通过正则校验或校验数据类型
                if "type" in value:
                    # 数据类型校验
                    type_str = value["type"]
                    if type_str == "N":
                        # 整形
                        if not isinstance(source_data, int):
                            error_info_dict[key] = source_data
                    elif type_str == "S":
                        # 字符串类型
                        if not isinstance(source_data, str):
                            error_info_dict[key] = source_data
                    elif type_str == "xxx":
                        # 扩展
                        pass

                elif "value" in value:
                    # 正则校验
                    reg_expression = value["value"]
                    print(reg_expression)
                    # rg = re.match(reg_expression, source_data)
                    # 做了类型转换，如果拿出的数据不是str类型，用正则匹配会报错：TypeError: expected string or bytes-like object，兼容这种情况
                    rg = re.match(reg_expression, "%s" % source_data)
                    if not reg_expression:
                        error_info_dict[key] = source_data

        return error_info_dict


if __name__ == "__main__":
    response_obj = {}
    check_point = {}
    print(CheckResult.check(response_obj, check_point))





