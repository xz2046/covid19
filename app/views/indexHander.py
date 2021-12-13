from tornado.web import RequestHandler

class IndexHander(RequestHandler):
    def get(self):
        self.write('hello')  #选择主页