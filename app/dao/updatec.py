import pandas as pd
from app.settings import engine


class UPdatec():
    def __init__(self):
        self.df_a = pd.read_sql('select * from ctoday;', engine)
        self.df_s = pd.read_sql('select * from ctodays;', engine)

    def bar(self):
        df = self.df_a.sort_values(by=['新增', '累计确诊'], ascending=False).head(6)
        bar_data = df['新增'].tolist()
        bar_name = df['省份'].tolist()
        return bar_data, bar_name

    def pie(self):
        z = zip(self.df_a['省份'], self.df_a['现有病例'])
        pie_data = []
        for item in z:
            c = {'name': item[0], 'value': item[1]}
            pie_data.append(c)
        return pie_data

    def cmap(self):
        z = zip(self.df_a['省份'], self.df_a['累计确诊'])
        map_data = []
        for item in z:
            c = {'name': item[0], 'value': item[1]}
            map_data.append(c)
        return map_data

    def run(self):
        bar_data, bar_name = self.bar()
        pie_data = self.pie()
        map_data = self.cmap()
        return [bar_data, bar_name, pie_data, map_data]
