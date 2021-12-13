from pymysql import connect

conn = connect(host="localhost",
               port=3306,
               user='root',
               password='*******',
               database='covid19',
               charset='utf8')
cs = conn.cursor()


def sums():
    cs.execute(
        'insert into cdatas (累计确诊,新增,治愈,死亡,现有病例,日期) select sum(累计确诊),sum(新增),sum(治愈),sum(死亡),sum(现有病例),日期 from cdata group by 日期;'
    )
    conn.commit()

    cs.close()
    conn.close()


def uptoday():
    cs.execute(
        'insert into cdata (日期,省份,累计确诊,现有病例,新增,治愈,死亡) select * from ctoday;')
    cs.execute(
        'insert into wdata (日期,国家,累计确诊,现有病例,新增,治愈,死亡,全称) select * from wtoday;'
    )
    cs.execute(
        'insert into cdatas (累计确诊,新增,死亡,治愈,现有病例,日期) select * from ctodays;')
    conn.commit()

    cs.close()
    conn.close()


#sums()  #注意 sums函数只执行一次
uptoday()