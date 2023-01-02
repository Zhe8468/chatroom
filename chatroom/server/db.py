from pymysql import connect
from config import *

class DB():
    """数据库管理类"""
    def __init__(self):
        # 创建连接
        self.conn = connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8'
        )
        # 获取游标
        self.cursor = self.conn.cursor()

    def get_info(self,sql):
        """查询用户信息"""
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取结果
        result = self.cursor.fetchone()
        # 判断是否有结果
        if not result:
            return None
        # 数据打包
        data = {}
        fileds = [filed[0] for filed in self.cursor.description]
        for filed,value in zip(fileds,result):
            data[filed] = value
        # 数据返回
        return data

    # 释放资源
    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    db = DB()
    data = db.get_info("select * from users WHERE user_name='user2'")
    print(data)
    db.close()