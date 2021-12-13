from app.views.indexHander import IndexHander
from app.views.homeHander import ChinaHander, WorldHander, UpdateC, UpdateW

urls = [(r'/', IndexHander), 
        (r'/yiqing', ChinaHander),
        (r'/yiqingworld', WorldHander), 
        (r'/updatec', UpdateC),
        (r'/updatew', UpdateW)]
