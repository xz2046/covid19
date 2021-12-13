from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from app.urls import urls
from app.settings import settings


#配置服务器
class customAPPlication(Application):
    def __init__(self):
        #url 设置地址不同地址调用函数情况
        # 从settings中获取配置并解包字典活动参数调用路径
        super(customAPPlication, self).__init__(urls, **settings)


def creater_server():
    server = HTTPServer(customAPPlication())  #传入参数
    #所有可用地址 localhost 127.0.0.1 IP地址
    server.listen(8800, address='0.0.0.0')  #设置端口和IP
    print('server is runing at 127.0.0.1:8800')
    IOLoop.current().start()  #开始启动服务器
