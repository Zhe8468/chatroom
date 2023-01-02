from config import *

# 响应登录请求
def response_login_result(result,username):
    """
    :param result: 返回登录结果 0表示失败 1表示成功
    """
    return SEPARATOR.join([RESPONSE_LOGIN_RESULT,str(result),username])

# 响应聊天请求
def response_chat_result(result,username,message):
    """
    :param result: 返回结果 0表示失败 1表示成功
    :param message: 消息的内容
    """
    return SEPARATOR.join([RESPONSE_CHAT,username,message])
