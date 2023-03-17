import pymysql
from dbutils.pooled_db import PooledDB
import pyperclip
from loguru import logger

import settings

CONFIG = settings.load_config()
db = CONFIG["db"]
host = db["host"]
user = db["user"]
password = db["password"]
database = db["database"]

# 创建连接池对象
pool = PooledDB(pymysql, 5, host=host, user=user, password=password, database=database)

# 从连接池中获取数据库连接对象
conn = pool.connection()

def insert_token(name):

    # 创建游标对象
    cursor = conn.cursor()

    # 获取复制板里的token
    token = pyperclip.paste()
    token = token.replace("\"", "")

    if len(token) > 0:
        logger.debug(token)
        sql = 'select * from test where name = %s'
        cursor.execute(sql, (name,))

        # 获取执行结果
        results = cursor.fetchall()
        for row in results:
            print(row)
    else:
        logger.error("复制板的token为空!")

    # 关闭游标和连接
    cursor.close()
    conn.close()



insert_token("nice boys")