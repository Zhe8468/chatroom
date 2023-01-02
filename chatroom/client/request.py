from config import *

# 请求登录结果
def request_login_result(username,password):
    """0001|user1|123456"""
    return SEPARATOR.join([REQUEST_LOGIN,username,password])

# 请求聊天结果
def request_chat(username,message):
    """0002|user1|内容"""
    return SEPARATOR.join([REQUEST_CHAT,username,message])

