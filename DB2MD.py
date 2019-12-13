# -*- coding:utf-8 -*-
from pymysql import OperationalError

from util.log_util import LogFactory
from util.db_util import DbUtil
import configparser
import os
import sys

current_path = os.path.dirname(os.path.realpath(sys.argv[0]))

config_file_path = current_path + r"/config.ini"

host = None
user = None
port = None
password = None
database = None
charset = None


def read_config_file():
    '''
    读取配置文件信息
    :return:
    '''
    if not os.path.isfile(config_file_path):
        logger.error("读取配置文件[%s]失败" % config_file_path)
        exit(1)
    cf = configparser.ConfigParser()
    cf.read(config_file_path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
    try:
        cf.items("mysql")
    except configparser.NoSectionError as e:
        logger.error(e.message)
        exit(1)

    try:
        global host
        global user
        global port
        global password
        global database
        global charset
        host = str(cf.get("mysql", "host")).strip()
        user = str(cf.get("mysql", "user")).strip()
        port = int(cf.get("mysql", "port"))
        password = str(cf.get("mysql", "password")).strip()
        database = str(cf.get("mysql", "database")).strip()
        charset = str(cf.get("mysql", "charset")).strip()
        DbUtil.connection = {"host": host, "user": user, "password": password, "database": database, "port": port,
                             "charset": charset}
    except configparser.NoOptionError as e:
        logger.error(e.message)
        exit(1)

    # 测试数据库连接是否正常
    test_sql = "select now()"
    try:
        DbUtil.query_one(test_sql)
    except OperationalError as e:
        logger.error(e)
        exit(1)


def init_config():
    read_config_file()


def get_table_list() -> list:
    global database
    sql = "select TABLE_NAME,ENGINE,TABLE_COLLATION,TABLE_COMMENT from information_schema.TABLES where table_schema = '%s' order by table_name" % database
    data_tables = DbUtil.query_all(sql)
    mysql_table_list = list()
    for table in data_tables:
        mysql_table_list.append(table)
    return mysql_table_list


logger = LogFactory.get_logger()
init_config()

md_file_path = current_path + "\\" + str(database) + ".md"
md_file = open(md_file_path, "w")
table_list = get_table_list()
for table_struct in table_list:
    table_name = table_struct["TABLE_NAME"]
    engine = table_struct["ENGINE"]

    md_file.write("## 表名:%s 存储引擎:%s 字符编码:%s 备注:%s \n" % (table_struct["TABLE_NAME"], table_struct["ENGINE"],
                                                         table_struct["TABLE_COLLATION"],
                                                         table_struct["TABLE_COMMENT"]))
    md_file.write("序号 | 字段 | 描述 | 类型 | 键类型 | 是否允许为NULL | 默认值 |\n")
    md_file.write("-|-|-|-|-|-|-\n")
    sql = "select * from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'" % (
        table_struct["TABLE_NAME"], database)
    table_struct_list = DbUtil.query_all(sql)
    for table_struct in table_struct_list:
        for key in table_struct:
            if table_struct[key] is None or table_struct[key] == "":
                table_struct[key] = "&nbsp;"
        md_file.write("%s | %s | %s | %s | %s | %s | %s |\n" % (
            table_struct["ORDINAL_POSITION"], table_struct["COLUMN_NAME"], table_struct["COLUMN_COMMENT"],
            table_struct["COLUMN_TYPE"], table_struct["COLUMN_KEY"], table_struct["IS_NULLABLE"],
            table_struct["COLUMN_DEFAULT"]))

    md_file.write("\n")
print("完成,生成文件路径为:%s" % md_file_path)
os.system('pause') #按任意键继续
