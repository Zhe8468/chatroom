# 局域网聊天室

## 测试环境
1. Python 3.8.5
2. NaviCat
3. PyCharm

## 虚拟环境
PipEnv

## 使用框架
1. 网络通讯：Socket
2. 界面：TTkboostrap
3. 多线程：Threading
4. 数据库 MySQL

## 功能
1. 多用户登录
2. 多线程局域网聊天
3. 支持实时显示在线人数


## 部署方式
采用Client+Brower的方式局域网部署

## 通讯协议
没有使用json或者xml，采用简单地自定义通讯文本
```
# 请求格式相关配置
REQUEST_LOGIN = "0001"
REQUEST_CHAT = "0002"
REQUEST_USERS = "0003"

#响应
RESPONSE_LOGIN_RESULT = "1001"
RESPONSE_CHAT = "1002"
RESPONSE_USERS = "1003"
SEPARATOR = "|"
```




