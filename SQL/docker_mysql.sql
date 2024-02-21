-- 1 , 创建一个表

# create table t_archer(
#   id int comment 'ID编号',
#   name char comment '英雄名称',
#   hp_max int comment '最大生命',
#   mp_max int comment '最大法力',
#   attack_max int comment '最高物攻',
#   defense_max int comment '最大防御',
#   attack_range char comment '攻击范围',
#   role_main char comment '主要定位',
#   role_assist char comment '次要定位'
# )
#   row_format
# row format delimited
# fields terminated by '\t';

create database test;


# LOAD DATA INFILE 命令
# https://blog.csdn.net/weixin_44377973/article/details/109266059


CREATE TABLE test.t_6(
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);

LOAD DATA LOCAL INFILE '/Users/linghuchong/Downloads/51/Python/project/SQL/text.txt' INTO TABLE test.t_6 FIELDS TERMINATED BY ',';


# Loading local data is disabled； this must be enabled on both the client and server sides解决方案
# https://blog.csdn.net/RoadYiL/article/details/125222516

show global variables like 'local_infile';

select * from test.t_6;



create table test.employee (
id int,
name varchar(50),
deg varchar(50),
salary int,
dept varchar(50));

create table test.employee_address (
id int,
hno varchar(50),
street varchar(50),
city varchar(50));

create table test.employee_connection (
id int,
phno varchar(50),
email varchar(50));

LOAD DATA LOCAL INFILE '/Users/linghuchong/Downloads/51/Python/project/SQL/employee.txt' INTO TABLE test.employee FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/Users/linghuchong/Downloads/51/Python/project/SQL/employee_address.txt' INTO TABLE test.employee_address FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/Users/linghuchong/Downloads/51/Python/project/SQL/employee_connection.txt' INTO TABLE test.employee_connection FIELDS TERMINATED BY ',';


select e.id,e.name,e_a.city,e_a.street
from test.employee e inner join test.employee_address e_a
on e.id = e_a.id;

select e.id,e.name,e_a.city,e_a.street
from test.employee e join test.employee_address e_a
on e.id = e_a.id;

select e.id,e.name,e_a.city,e_a.street
from test.employee e ,test.employee_address e_a
where e.id = e_a.id;


select e.id,e.name,e_conn.phno, e_conn.email
from test.employee e left join test.employee_connection e_conn
on e.id = e_conn.id;

select e.id,e.name,e_conn.phno, e_conn.email
from test.employee e left outer join test.employee_connection e_conn
on e.id = e_conn.id;


select e.id,e.name,e_conn.phno, e_conn.email
from test.employee e right join test.employee_connection e_conn
on e.id = e_conn.id;


show function code;

describe function extended count;

select length("123");
select reverse("abc");
select concat("angela",'baby');

# select concat_ws('.','www', array('itcast','cn'));

select substr("123456", -2);
select substr("123456", 2,2);

# select split('apache hive', '')

select current_date();

select unix_timestamp();

select unix_timestamp('2011-12-07 12:23:12');
select from_unixtime(1323260592);

# select date_add('2012-11-28', 3);
# select date_sub('2012-12-12', 1);

select datediff('2020-12-12', '2020-12-11');
# select from_unixtime(0, 'yyyy-MM-dd HH:mm:ss');


select round(3.1415926);
select round(3.1415926, 4);
select rand();
select rand(3);

select * from test.employee limit 2;


select if(1=2,100,200)；
select if(id = 1202 , 'M', 'W') from test.employee;

# 空值转换
# select nvl("alen", "itcaset")

# 条件转换
select case 100 when 50 then 'tom' when 100 then 'mary' else 'tim' end as t;



show columns from test.employee

show keys from test.employee;
show index from test.employee;
show view;
show trigger;

show functions;


select * from test.employee;

# ctas
create table test.e1 as select  deg,name from test.employee limit 3;

select * from test.e1