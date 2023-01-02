import socket
from threading import Thread
from config import *
from response import *
from db import DB


class Server():
    """服务器核心类"""

    def __init__(self):
        """套接字初始化"""
        # 创建TCP套接字
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((SERVER_IP, SERVER_PORT))
        self.server.listen(128)
        # 初始化客户端字典
        self.clients = {}
        # 初始化数据库管理对象
        self.db = DB()

    def begin(self):
        """获取客户端连接并提供服务"""
        while True:
            # 监听客户端连接
            print("正在监听客户端...")
            client, addr = self.server.accept()
            print("接收到客户端连接!")
            # 开启子线程为客户端提供服务
            Thread(target=self.recept_client, args=(client, addr)).start()

    def recept_client(self, client, addr):
        """收发客户端数据"""
        while True:
            # 接收客户端数据
            try:
                recv_data = client.recv(1024).decode("utf-8")
            except:
                return ""
            # 没接收到内容 关闭客户端套接字
            if not recv_data:
                self.remove_user(client)
                client.close()
                break
            # 解析数据
            data = self.parse_data(recv_data)
            # 分析请求类型 直接执行不同的响应函数
            if data["id"] == REQUEST_LOGIN:
                self.login_handler(client, data)
            elif data["id"] == REQUEST_CHAT:
                self.chat_handler(client, data)
            elif data['id'] == REQUEST_USERS:
                self.remove_user(client)
                self.update_tree()

    def parse_data(self, recv_data):
        """
        解析客户端数据
        登录格式：0001|username|password
        消息格式：0002|username|message
        更新格式：0003|
        """
        result = {}
        # 获取请求类型
        result["id"] = recv_data.split("|")[0]
        # 用户请求登录
        if result["id"] == REQUEST_LOGIN:
            result["username"] = recv_data.split("|")[1]
            result["password"] = recv_data.split("|")[2]
        # 聊天
        elif result["id"] == REQUEST_CHAT:
            result["username"] = recv_data.split("|")[1]
            result["message"] = recv_data.split("|")[2]
        elif result['id'] == REQUEST_USERS:
            pass
        # 返回解析成功的数据
        return result

    def login_handler(self, client, data):
        """
        处理登录请求
        0表示用户不存在
        1表示密码错误
        2表示登录成功
        """
        # 获取账号密码
        username = data.get("username")
        password = data.get("password")
        # 检查登录
        res, username = self.check_login(username, password)
        # 登录成功保存
        if res == "2":
            self.clients[username] = {"client": client}
            # 发送当前在线用户字典
            self.update_tree()
        # 返回响应信息
        result = response_login_result(res, username)
        client.send(result.encode("utf-8"))

    def check_login(self, username, password):
        """
        检查是否登录成功，并且返回状态，昵称和用户名
        0表示用户不存在
        1表示密码错误
        2表示登录成功
        """
        # 数据库查询
        result = self.db.get_info("select * from users where user_name='%s'" % format(username))
        if not result:
            return '0', ''
        if password != result['user_password']:
            return '1', ''
        return '2', result['user_name']

    def chat_handler(self, client, data):
        """处理聊天功能"""
        # 获取消息内容
        username = data.get("username")
        message = data.get('message')
        # 响应消息
        result = response_chat_result(RESPONSE_CHAT, username, message)
        # 转发给在线用户
        for u_name, dict in self.clients.items():
            if u_name == username:
                continue
            cli = dict["client"]
            cli.send(result.encode("utf-8"))

    def remove_user(self, client):
        """客户端下线处理"""
        print(self.clients.keys())
        for u_name, dict in self.clients.items():
            cli = dict["client"]
            if cli == client:
                del self.clients[u_name]
                break

    def update_tree(self):
        """
        处理在线用户更新
        """
        # 合成响应文本
        usernames = ",".join(list(self.clients.keys()))
        result = RESPONSE_USERS + "|" + usernames
        # 转发给在线用户
        for u_name, dic in self.clients.items():
            cli = dic["client"]
            cli.send(result.encode("utf-8"))


if __name__ == '__main__':
    server = Server()
    server.begin()
