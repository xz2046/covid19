from tornado.web import RequestHandler
import json

from app.chart.get_chinacharts import GetChart
from app.chart.get_worldcharts import GetCahrtWorld
from app.dao.updatec import UPdatec
from app.dao.updatew import UPdatew

class ChinaHander(RequestHandler):
    def get(self):
        getmap = GetChart()
        html = getmap.run()
        self.render('yiqing.html', x = {'html': html}) 

class WorldHander(RequestHandler):
    def get(self):
        getmap = GetCahrtWorld()
        html = getmap.run()
        self.render('yiqingworld.html', x = {'html': html}) 

class UpdateC(RequestHandler):   
    def get(self):                  
        upd = UPdatec()
        values = upd.run()
        self.write(json.dumps(values))

class UpdateW(RequestHandler):   
    def get(self):                  
        upd = UPdatew()
        values = upd.run()
        self.write(json.dumps(values))