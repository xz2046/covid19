from sqlalchemy.ext.declarative import declarative_base  #数据库建模
from sqlalchemy import Column, INTEGER, Date, DateTime
from link import engine


Base = declarative_base()

order = ['现有病例', '累计确诊', '新增', '治愈', '死亡', '日期', '最新更新时间']


class Province(Base):
    __tablename__ = 'wtodays'
    现有病例 = Column(INTEGER)
    累计确诊 = Column(INTEGER)
    新增 = Column(INTEGER)
    治愈 = Column(INTEGER)
    死亡 = Column(INTEGER)
    日期 = Column(Date, primary_key=True)
    更新 = Column(DateTime)


if __name__ == '__main__':
    #创建表格
    Base.metadata.create_all(engine)
