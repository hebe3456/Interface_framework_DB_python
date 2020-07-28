最终版
数据表和数据存储结构
interface_api;
+--------+----------+------------------------------------------+----------+--------+--------+---------------------+
| api_id | api_name | r_url                                    | r_method | p_type | status | ctime               |
+--------+----------+------------------------------------------+----------+--------+--------+---------------------+


interface_data_store
+--------+----------+------------------------------------------+---------------------+
| api_id | case_id | data_store                                | ctime               |
+--------+----------+------------------------------------------+---------------------+


interface_test_case;
+----+--------+-----------------------------------------------------------------------------+-----------------------------------------------------+----------------------+----------------------+----------------------+---------------------------------------------------------+------------+--------+-------+
| id | api_id | request_data                                                                | request_rely_data                                           | expect_response_code | expect_response_body | actual_response_body | data_store_rule  (包含 request + response两部分)         | error_info | status | ctime |
+----+--------+-----------------------------------------------------------------------------+-----------------------------------------------------+----------------------+----------------------+----------------------+---------------------------------------------------------+------------+--------+-------+


创建数据库create database if not exists interface_autotest default charset utf8 collate utf8_general_ci;

create table interface_api(
api_id int not null auto_increment comment "自增长主键",
api_name varchar(50) not null comment "接口名称",
r_url varchar(50) not null comment "请求接口的URL",
    r_method varchar(10) not null comment "接口请求方式",
    p_type varchar(20) not null comment "传参方式",
    status tinyint default 0,
    ctime datetime,
    unique index(api_name),
    primary key(api_id)
)engine=InnoDB default charset=utf8;

create table interface_test_case(
    id int not null AUTO_INCREMENT comment "自增长主键",
    api_id int not null comment "对应interface_api的api_id",
    request_data varchar(255) comment "请求接口时传入的参数",
    request_rely_data varchar(255) comment "请求接口时依赖的数据",
    expect_response_code int comment "接口期望响应code",
    expect_response_body varchar(255) comment "接口期望响应body校验数据点",
    actual_response_body varchar(255) comment "接口实际响应body",
    data_store_rule varchar(255) comment "依赖数据存储",
    error_info varchar(1000) comment "错误信息列",
    status tinyint default 0 comment "用例执行状态，0不执行，1执行",
    ctime datetime,
    primary key(id),
    index(api_id)
)engine=InnoDB default charset=utf8;

create table interface_data_store(
    api_id int not null comment "对应interface_api的api_id",
    case_id int not null comment "对应interface_test_case里面的id",
    data_store varchar(255) comment "存储的依赖数据",
    ctime datetime,
    index(api_id,case_id)
)engine=InnoDB default charset=utf8;



