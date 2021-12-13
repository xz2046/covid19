import time
import json
import requests
import pandas as pd
from link import engine


df = pd.read_sql('select * from chinaurl', engine)


def get_china_data():
    all_url = list(df['地址'])
    name = list(df['省份'])
    errorNum = 0
    insertValue = []
    for i in range(0, len(name)):
        provinceName = name[i]
        url = all_url[i]
        try:

            proxies = {
                "http": "167.172.180.46:33555"  # 代理ip
            }
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }

            r = requests.get(url, timeout=30, headers=headers, proxies=proxies)
            r.raise_for_status()
            r.encoding = 'utf-8'
            provinceJson = json.loads(r.text)
            for j in range(0, len(provinceJson['data'])):
                tupleData = ()
                tupleData += (provinceJson['data'][j]['confirmedCount'],
                              provinceJson['data'][j]['confirmedIncr'],
                              provinceJson['data'][j]['curedCount'],
                              provinceJson['data'][j]['currentConfirmedCount'],
                              provinceJson['data'][j]['dateId'],
                              provinceJson['data'][j]['deadCount'],
                              provinceName)
                insertValue.append(tupleData)
            time.sleep(10)
        except:
            errorNum += 1
            print("在获取 " + provinceName + " 数据时出错！")
    name = ['累计确诊', '新增', '治愈', '现有病例', '日期', '死亡', '省份']
    df1 = pd.DataFrame(data=insertValue, columns=name)
    order = ['日期', '省份', '累计确诊', '现有病例', '新增', '治愈', '死亡']
    df1['日期'] = pd.to_datetime(df1['日期'].astype(str))
    df1 = df1[order]
    df1.to_sql('cdata', engine, if_exists='append', index=False)
    print("各省数据获取完成！")
    print("错误数据量为：" + str(errorNum))


get_china_data()
