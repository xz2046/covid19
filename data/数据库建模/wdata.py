from sqlalchemy.ext.declarative import declarative_base  #数据库建模
from sqlalchemy import Column, VARCHAR, INTEGER, Date
from link import engine

Base = declarative_base()

order = ['日期', '国家', '累计确诊', '现有病例', '新增', '治愈', '死亡', '全称']


class Province(Base):
    __tablename__ = 'wdata'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    日期 = Column(Date)
    国家 = Column(VARCHAR(50))
    累计确诊 = Column(INTEGER)
    现有病例 = Column(INTEGER)
    新增 = Column(INTEGER)
    治愈 = Column(INTEGER)
    死亡 = Column(INTEGER)
    全称 = Column(VARCHAR(100))


if __name__ == '__main__':
    #创建表格
    Base.metadata.create_all(engine)
