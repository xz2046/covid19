import requests, json
import pandas as pd
import datetime

from 国家英文名对照表 import english_name
from link import engine

class GetData():
    def __init__(self) -> None:
        self.engine = engine
        self.times = datetime.datetime.now()
        self.today = self.times.date()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.sumchinadata = []

        #获取世界数据
        res1 = requests.get(
            'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=WomWorld,WomAboard'
        )
        res_json1 = json.loads(res1.text)['data']
        self.worldData = res_json1['WomAboard']
        self.worldSum = res_json1['WomWorld']

        #获取国内数据
        res = requests.get(
            'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5')
        res_json2 = json.loads(res.json()['data'])
        self.chinaSum = res_json2['areaTree'][0]['name'], res_json2[
            'areaTree'][0]['today'], res_json2['areaTree'][0]['total']
        self.chinaData = res_json2['areaTree'][0]['children']

    def get_worldSum(self):  #获取世界总体数据
        worldSum = self.worldSum
        name = ['现有病例', '累计确诊', '新增', '治愈', '死亡', '日期', '最新更新时间']

        sumdata = [[
            worldSum['nowConfirm'], worldSum['confirm'],
            worldSum['confirmAdd'], worldSum['heal'], worldSum['dead'],
            worldSum['PubDate'], worldSum['lastUpdateTime']
        ]]

        df_world_sum = pd.DataFrame(sumdata, columns=name)
        df_world_sum['日期'] = pd.to_datetime(df_world_sum['日期'])
        df_world_sum.set_index(df_world_sum['日期'], inplace=True)
        return df_world_sum

    def get_chinaSum(self):  #获取国内总体数据
        chinasum = self.chinaSum
        name = ['累计确诊', '新增', '死亡', '治愈', '现有病例', '日期']
        china_sumdata = [[
            chinasum[2]['confirm'], chinasum[1]['confirm'],
            chinasum[2]['dead'], chinasum[2]['heal'],
            chinasum[2]['nowConfirm'],
            pd.to_datetime(self.today)
        ]]
        self.sumchinadata = [
            chinasum[2]['confirm'], chinasum[1]['confirm'],
            chinasum[2]['dead'], chinasum[2]['heal'],
            chinasum[2]['nowConfirm'],
            pd.to_datetime(self.today), 'China'
        ]
        df_china_sum = pd.DataFrame(china_sumdata, columns=name)
        return df_china_sum

    def get_worldData(self):  #获取世界国家数据
        worldData = self.worldData
        data = []
        for child in worldData:
            a = child['name'], child['confirm'], child['confirmAdd'], child[
                'dead'], child['heal'], child['nowConfirm'], child['pub_date']
            data.append(a)
        name = ['国家', '累计确诊', '新增', '死亡', '治愈', '现存确诊', '日期']
        order = ['日期', '国家', '累计确诊', '现存确诊', '新增', '治愈', '死亡', '全称']
        df_world = pd.DataFrame(data, columns=name)
        df_world['日期'] = pd.to_datetime(df_world['日期'])
        df_world.set_index('国家', inplace=True)
        for i, j in english_name.items():
            df_world.loc[j, '全称'] = i
        df_world.loc['中国'] = self.sumchinadata

        df_world['国家'] = df_world.index
        df_world = df_world[order]
        return df_world

    def get_chinaData(self):  #获取国内省份数据
        chinadata = self.chinaData
        data = []
        for child in chinadata:
            a = self.today, child['name'], child['today']['confirm'], child[
                'total']['nowConfirm'], child['total']['confirm'], child[
                    'total']['dead'], child['total']['heal']
            data.append(a)
        name = ['日期', '省份', '新增', '现有病例', '累计确诊', '死亡', '治愈']
        order = ['日期', '省份', '累计确诊', '现有病例', '新增', '治愈', '死亡']
        df_chain = pd.DataFrame(columns=name, data=data)
        df_chain = df_chain[order]
        return df_chain

    def save_sql(self):
        try:
            self.get_chinaSum().to_sql('ctodays',
                                       self.engine,
                                       if_exists='replace',
                                       index=False)
        except:
            print('添加中国总体数据出现错误')
        try:
            self.get_worldSum().to_sql('wtodays',
                                       self.engine,
                                       if_exists='replace',
                                       index=False)
        except:
            print('添加全球总体数据出现错误')

        try:
            self.get_chinaData().to_sql('ctoday',
                                        self.engine,
                                        if_exists='replace',
                                        index=False)
        except:
            print('添加中国省份数据出现错误')
        try:
            self.get_worldData().to_sql('wtoday',
                                        self.engine,
                                        if_exists='replace',
                                        index=False)
        except:
            print('添加全球国家数据出现错误')


gd = GetData()
gd.save_sql()
