import time
import json
import requests
import pandas as pd
from sqlalchemy import create_engine

from link import engine

df = pd.read_sql('select * from worldurl', engine)


def get_world_data():
    all_url = list(df['地址'])
    name = list(df['名称'])
    fullname = list(df['全称'])
    errorNum = 0
    insertValue = []
    for i in range(0, len(name)):
        countryName = name[i]
        countryFullName = fullname[i]
        url = all_url[i]
        try:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }

            r = requests.get(url, timeout=30, headers=headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            countryJson = json.loads(r.text)
            for j in range(0, len(countryJson['data'])):
                tupleData = ()
                tupleData += (countryJson['data'][j]['confirmedCount'],
                              countryJson['data'][j]['confirmedIncr'],
                              countryJson['data'][j]['curedCount'],
                              countryJson['data'][j]['currentConfirmedCount'],
                              countryJson['data'][j]['dateId'],
                              countryJson['data'][j]['deadCount'], countryName,
                              countryFullName)
                insertValue.append(tupleData)
            time.sleep(10)
        except:
            errorNum += 1
            print("在获取 " + countryName + " 数据时出错！")
    name = ['累计确诊', '新增', '治愈', '现有病例', '日期', '死亡', '国家', '全称']
    df1 = pd.DataFrame(data=insertValue, columns=name)
    order = ['日期', '国家', '累计确诊', '现有病例', '新增', '治愈', '死亡', '全称']
    df1['日期'] = pd.to_datetime(df1['日期'].astype(str))
    df1 = df1[order]
    #print(df1)
    df1.to_sql('wdata', engine, if_exists='append', index=False)
    print("各国数据获取完成！")
    print("错误数据量为：" + str(errorNum))


get_world_data()