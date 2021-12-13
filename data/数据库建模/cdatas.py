from sqlalchemy.ext.declarative import declarative_base  #数据库建模
from sqlalchemy import Column, INTEGER, Date
from link import engine


Base = declarative_base()

order = ['累计确诊', '新增', '死亡', '治愈', '现有病例', '日期']


class Province(Base):
    __tablename__ = 'cdatas'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    累计确诊 = Column(INTEGER)
    新增 = Column(INTEGER)
    治愈 = Column(INTEGER)
    死亡 = Column(INTEGER)
    现有病例 = Column(INTEGER)
    日期 = Column(Date)


if __name__ == '__main__':
    #创建表格
    Base.metadata.create_all(engine)
