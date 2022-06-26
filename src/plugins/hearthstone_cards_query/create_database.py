from .config import DATABASE_NAME, DATABASE_PASSWORD, DATABASE_CHARSET, DATABASE_HOST, DATABASE_PORT, DATABASE_USER

import pymysql


def create_database():
    """python + pymysql 创建数据库"""

    # 创建连接
    conn = pymysql.connect(host=DATABASE_HOST,
                           user=DATABASE_USER,
                           password=DATABASE_PASSWORD,
                           port=DATABASE_PORT,
                           charset=DATABASE_CHARSET)
    # 创建游标
    cursor = conn.cursor()

    # 创建数据库的sql(如果数据库存在就不创建，防止异常)
    sql = "DROP DATABASE IF EXISTS " + DATABASE_NAME
    # 执行删除数据库的sql
    cursor.execute(sql)

    sql = "CREATE DATABASE IF NOT EXISTS " + DATABASE_NAME
    # 执行创建数据库的sql
    cursor.execute(sql)
