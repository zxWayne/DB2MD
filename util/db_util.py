# -*- coding:utf-8 -*-
import pymysql
import contextlib
from util.log_util import LogFactory

logger = LogFactory.get_logger()


class DbUtil:
    # 连接配置
    connection = {}

    # 定义上下文管理器，连接后自动关闭连接
    @staticmethod
    @contextlib.contextmanager
    def mysql():
        if len(DbUtil.connection) <= 0:
            raise RuntimeError("未初始化连接配置")
        host = DbUtil.connection.get("host")
        port = DbUtil.connection.get("port")
        user = DbUtil.connection.get("user")
        password = DbUtil.connection.get("password")
        database = DbUtil.connection.get("database")
        charset = DbUtil.connection.get("charset")

        conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database, charset=charset)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            yield cursor
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    @staticmethod
    def execute(sql):
        logger.debug(sql)
        with DbUtil.mysql() as cursor:
            row_count = cursor.execute(sql)
            return row_count

    @staticmethod
    def query_one(sql: str) -> dict:
        """
        查询一条数据
        :param sql:
        :return:
        """
        logger.debug(sql)
        with DbUtil.mysql() as cursor:
            cursor.execute(sql)
            data = cursor.fetchone()
            return data

    @staticmethod
    def query_all(sql: str) -> list:
        """
        查询所有的数据
        :param sql:
        :return:
        """
        logger.debug(sql)
        with DbUtil.mysql() as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
            return data


if __name__ == '__main__':
    connection = {
        "host": 'localhost',
        "port": 3306,
        "user": 'root',
        "password": 'root',
        "database": 'test',
        "charset": 'utf8'
    }

    DbUtil.connection = connection
    a = DbUtil.execute("insert into tb_role (remarks,role_name) value ('aa','bb')")

    print(type(a))
