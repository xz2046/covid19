import pandas as pd
from app.settings import engine


class UPdatew():
    def __init__(self):
        self.df_a = pd.read_sql('select * from wtoday;', engine)

    def wmap(self):
        z = zip(self.df_a['全称'], self.df_a['累计确诊'])
        map_data = []
        for item in z:
            c = {'name': item[0], 'value': item[1]}
            map_data.append(c)
        return map_data

    def pie(self):
        df_pie = self.df_a.sort_values('现存确诊', ascending=False).head(20)
        z = zip(df_pie['国家'], df_pie['现存确诊'])
        pie_data = []
        for item in z:
            c = {'name': item[0], 'value': item[1]}
            pie_data.append(c)
        return pie_data

    def run(self):
        map_data = self.wmap()
        pie_data = self.pie()
        return [map_data, pie_data]
