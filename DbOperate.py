import pymysql
from dbutils.pooled_db import PooledDB
from loguru import logger

import settings
from error.DbExcept import DbExcept

CONFIG = settings.load_config()
db = CONFIG["db"]
host = db["host"]
user = db["user"]
password = db["password"]
database = db["database"]

# 创建连接池对象
pool = PooledDB(pymysql, 5, host=host, user=user, password=password, database=database)


def check_conn():
    # 从连接池中获取数据库连接对象
    conn = pool.connection()

    # 获取游标对象
    cursor = conn.cursor()

    # 执行查询
    cursor.execute("SELECT 1")

    # 获取结果
    result = cursor.fetchone()

    # 关闭游标和连接
    cursor.close()
    conn.close()

    # 返回结果
    return result is not None

def insert_token(name, token, invite_url):
    # 从连接池中获取数据库连接对象
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    if len(token) > 0 and len(invite_url) > 0:
        logger.debug(token)
        sql = "select id from ar_invitaion_link where link = %s"
        cursor.execute(sql, (invite_url,))

        # 获取执行结果
        link_id = cursor.fetchone()
        if link_id is None:
            raise DbExcept("获取链接id失败!")
        logger.debug(f"获取link_id={link_id[0]}")

        # 写入token
        sql = "insert into ar_token (user_name, user_token, ar_invitation_link_id) values (%s, %s, %s)"
        a = cursor.execute(sql, (name, token, link_id[0]))
        logger.debug(f"token={token},写入成功！")

    else:
        logger.error("复制板的token或邀请链接为空!")
    conn.commit()
    # 关闭游标和连接
    cursor.close()
    conn.close()

# insert_token("mCnXJxKcy472090", "MTA4NjU3NDg1OTE1ODU1Njc1NA.GZMT_9.ahc8v1xVBZYBAC0wF8nQ9YIx5bSYf-47WHtnTk", "https://discord.gg/VRDPVSr3wf")