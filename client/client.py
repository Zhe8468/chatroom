import socket, window_login, window_chat, time, ttkbootstrap as ttk, sys
from tkinter.messagebox import showinfo
from request import *
from config import *
from threading import Thread


class Client():
    """客户端核心类"""

    def __init__(self):
        """套接字初始化"""
        # 创建TCP套接字
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务器
        self.client.connect((SERVER_IP, SERVER_PORT))

    def begin(self):
        """初始化客户端资源"""
        # 初始化登录窗口
        self.login_window = window_login.LoginWindow()
        self.login_window.button1['command'] = self.on_login_button
        self.login_window.button2['command'] = self.on_clear_button
        self.login_window.root.protocol("WM_DELETE_WINDOW", self.on_window_closed)

        # 初始化聊天窗口
        self.chat_window = window_chat.ChatWindow()
        self.chat_window.toplevel.master = self.login_window.root
        self.chat_window.button['command'] = self.on_send_click
        self.chat_window.toplevel.protocol("WM_DELETE_WINDOW", self.on_window_closed)
        self.chat_window.toplevel.withdraw()

        # 初始化用户名
        self.username = None

        # 创建接收消息的子线程
        Thread(target=self.recept_server).start()
        # 进入窗口主循环
        self.login_window.root.mainloop()

    def recept_server(self):
        """接收服务器发送过来的消息"""
        while True:
            # 接收服务器响应回来的数据
            recv_data = self.client.recv(1024).decode("utf-8")
            # 解析服务器响应回来的数据
            data = self.parse_data(recv_data)
            # 根据消息内容分别处理
            if data['id'] == RESPONSE_LOGIN_RESULT:
                self.login_handler(data)
            elif data['id'] == RESPONSE_CHAT:
                self.chat_handler(data)
            elif data['id'] == RESPONSE_USERS:
                self.update_tree(data)

    def on_clear_button(self):
        """清空输入框"""
        self.login_window.entry1.delete(0, ttk.END)
        self.login_window.entry2.delete(0, ttk.END)

    def on_login_button(self):
        """发送用户名和密码到服务器"""
        # 获取用户名和密码
        username = self.login_window.entry1.get()
        password = self.login_window.entry2.get()
        # 生成协议文本
        result = request_login_result(username, password)
        # 发送到服务器
        self.client.send(result.encode("utf-8"))

    def parse_data(self, recv_data):
        """
        解析服务器的响应数据
        登录：1001|状态|用户名
        聊天：1002|用户名|消息
        字典：1003|用户名...
        """
        # 切割消息
        recv_data_list = recv_data.split(SEPARATOR)
        # 解析消息内容
        result = dict()
        result['id'] = recv_data_list[0]
        # 将消息内容处理进字典
        if result['id'] == RESPONSE_LOGIN_RESULT:
            result['state'] = recv_data_list[1]
            result['username'] = recv_data_list[2]
        elif result['id'] == RESPONSE_CHAT:
            result['username'] = recv_data_list[1]
            result['message'] = recv_data_list[2]
        elif result['id']==RESPONSE_USERS:
            result['users'] = recv_data_list[1]
        # 将解析完成的数据返回
        return result

    def login_handler(self, data):
        """登录结果响应"""
        # 判断是否登录成功
        print(data['state'])
        if data['state'] == '0':
            showinfo(message="登录失败,用户不存在", title="提示")
            return
        elif data['state'] == '1':
            showinfo(message="登录失败,密码错误", title="提示")
            return
        # 保存用户名
        self.username = data['username']
        # 登录成功显示聊天窗口
        self.chat_window.toplevel.update()
        self.chat_window.toplevel.deiconify()
        self.login_window.root.withdraw()
        self.set_title(self.username)
        # 提示用户登陆成功
        showinfo(message="登录成功!", title="提示")

    def chat_handler(self, data):
        """聊天消息响应"""
        sender = data['username']
        message = data['message']
        self.add_message(sender, message)

    def set_title(self, username):
        """设置标题"""
        self.chat_window.toplevel.title("欢迎{}进入聊天室！".format(username))

    def on_send_click(self):
        """设置标题"""
        # 获取聊天内容
        content = self.get_content()
        # 清空
        self.clear_content()
        # 添加内容到界面
        self.add_message("我", content)
        # 拼接协议文本
        text = request_chat(self.username, content)
        # 发送到服务器
        self.client.send(text.encode("utf-8"))

    def get_content(self):
        """设置标题"""
        return self.chat_window.text.get(0.0, ttk.END)

    def clear_content(self):
        """设置标题"""
        return self.chat_window.text.delete(0.0, ttk.END)

    def add_message(self, sender, message):
        """添加消息到聊天区"""
        info = "{}：{}\n".format(sender, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        self.chat_window.char_area.insert(ttk.END, info, 'blue')
        self.chat_window.char_area.insert(ttk.END, "  " + message, 'white')
        self.chat_window.char_area.yview_scroll(3, ttk.UNITS)

    def update_tree(self,data):
        """更新在线用户"""
        print("更新！")
        # 先清空原来的tree
        for child in self.chat_window.tree.get_children():
            self.chat_window.tree.delete(child)
        # 更新tree
        users = data['users'].split(',')
        for user in users:
            self.chat_window.tree.insert('', ttk.END, values=(user,))



    def on_window_closed(self):
        """关闭窗口的资源释放"""
        # 服务器更新在线用户
        self.client.send("0003|".encode("utf-8"))
        # 释放资源
        self.client.close()
        sys.exit(0)



if __name__ == '__main__':
    client = Client()
    client.begin()
