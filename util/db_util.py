# -*- coding:utf-8 -*-
import pymysql
import contextlib
from util.log_util import LogFactory
from abc import ABCMeta, abstractmethod
import cx_Oracle as cx

logger = LogFactory.get_logger()


class AbstractDbUtil(metaclass=ABCMeta):
    conn = None
    cursor = None

    # 连接配置
    connection = {}

    @abstractmethod
    def init(self, con_config):
        pass

    @abstractmethod
    def execute(self, sql: str):
        pass

    @abstractmethod
    def query_one(self, sql: str) -> dict:
        pass

    @abstractmethod
    def query_all(self, sql: str) -> list:
        pass


class OracleDbUtil(AbstractDbUtil):

    def __init__(self, con_config):
        self.init(con_config)

    @contextlib.contextmanager
    def init(self, con_config):

        host = con_config.get("host")
        port = con_config.get("port")
        user = con_config.get("user")
        password = con_config.get("password")
        database = con_config.get("database")
        charset = con_config.get("charset")
        conn_str = host + ':' + str(port) + '/' + database
        self.conn = cx.connect(user, password, conn_str)
        self.cursor = self.conn.cursor()

    def execute(self, sql: str):
        logger.debug(sql)
        row_count = self.cursor.execute(sql)
        return row_count

    def query_one(self, sql: str) -> dict:
        """
        查询一条数据
        :param sql:
        :return:
        """
        logger.debug(sql)

        self.cursor.execute(sql)
        cols = [d[0] for d in self.cursor.description]
        data = self.cursor.fetchone()
        data = dict(zip(cols, data))
        return data

    def query_all(self, sql: str) -> list:
        """
        查询所有的数据
        :param sql:
        :return:
        """
        logger.debug(sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        cols = [d[0] for d in self.cursor.description]
        result = list()
        for row in data:
            result.append(dict(zip(cols, row)))
        return result

    def __del__(self):
        self.cursor.close()
        self.conn.close()


class MysqlDbUtil(AbstractDbUtil):
    # 连接配置

    def __init__(self, con_config):
        self.init(con_config)

    # 定义上下文管理器，连接后自动关闭连接
    @contextlib.contextmanager
    def init(self, con_config):

        host = con_config.get("host")
        port = con_config.get("port")
        user = con_config.get("user")
        password = con_config.get("password")
        database = con_config.get("database")
        charset = con_config.get("charset")

        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def execute(self, sql):
        logger.debug(sql)
        row_count = self.cursor.execute(sql)
        return row_count

    def query_one(self, sql: str) -> dict:
        """
        查询一条数据
        :param sql:
        :return:
        """
        logger.debug(sql)

        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data

    def query_all(self, sql: str) -> list:
        """
        查询所有的数据
        :param sql:
        :return:
        """
        logger.debug(sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    connection = {
        "host": 'localhost',
        "port": 3306,
        "user": 'root',
        "password": 'root',
        "database": 'test',
        "charset": 'utf8'
    }

    util = MysqlDbUtil(connection)
    a = util.query_all(" select * from tb_user")

    print(a)
