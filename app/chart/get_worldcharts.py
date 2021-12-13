import pandas as pd

from pyecharts.charts import Map, Pie, Page
import pyecharts.options as opts
from pyecharts.components import Table
from app.settings import engine, settings
from app.chart.国家英文名对照表 import english_name

color = [
    '#D87C7C', '#919E8B', '#D7AB82', '#6E7074', '#61A0A8', '#EFA18D',
    '#787464', '#CC7E63', '#724E58', '#4B565B', '#D87C7C', '#919E8B',
    '#D7AB82', '#6E7074', '#61A0A8'
]
pieces = [{
    'value': 0,
    'color': '#F5F5F5'
}, {
    'min': 1,
    'max': 99
}, {
    'min': 100,
    'max': 999
}, {
    'min': 1000,
    'max': 9999
}, {
    'min': 10000,
    'max': 99999
}, {
    'min': 100000,
    'max': 499999
}, {
    'min': 500000,
    'lable': '50000人及以上'
}]


class GetCahrtWorld():
    def __init__(self) -> None:

        self.df = pd.read_sql('select * from wtoday;', engine)
        self.df['日期'] = self.df['日期'].astype('datetime64')
        self.df.set_index('日期', inplace=True)
        self.df_all = pd.read_sql('select * from wtodays;',
                                  engine).set_index('日期')

    def get_map(self):
        df_map = self.df
        map_chart = (Map(init_opts=opts.InitOpts(chart_id='02001')).add(
            '累计确诊',
            list(zip(df_map['国家'], df_map['累计确诊'])),
            'world',
            name_map=english_name,
            max_scale_limit=1.5,
            min_scale_limit=0.8,
            is_map_symbol_show=False).set_global_opts(
                title_opts=opts.TitleOpts(
                    title="全球疫情实时数据平台",
                    pos_left='center',
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_weight='bold', font_size=36, font_family='华文楷体')),
                legend_opts=opts.LegendOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(max_=70000,
                                                  is_piecewise=True,
                                                  pieces=pieces),
            ).set_series_opts(label_opts=opts.LabelOpts(is_show=False)))
        return map_chart

    def get_pie(self):
        df_pie = self.df.sort_values('现存确诊', ascending=False).head(20)
        pie_chart = (Pie(init_opts=opts.InitOpts(chart_id='02002')).add(
            '现存确诊',
            data_pair=list(zip(df_pie['国家'], df_pie['现存确诊'])),
            radius=['35%', '65%'],
            label_opts=opts.LabelOpts(
                is_show=True)).set_colors(color).set_global_opts(
                    legend_opts=opts.LegendOpts(is_show=False),
                    title_opts=opts.TitleOpts('全球现存确诊TOP20',
                                              pos_left='center',
                                              pos_top='top')))
        return pie_chart

    def get_table(self):
        table_chart = Table()
        table_chart.chart_id = '01006'
        headers = ["累计确诊", "累计死亡", "现有确诊", "今日新增"]
        rows = [[
            int(self.df_all['累计确诊']),
            int(self.df_all['死亡']),
            int(self.df_all['现有病例']),
            int(self.df_all['新增'])
        ]]
        table_chart.add(
            headers,
            rows,
            attributes={
                'style':
                'font-size: 28px;color:#363636;text-align:center;font-family:宋体;font-weight:bold;'
            })

        return table_chart

    def run(self):
        page = Page()
        page.add(self.get_map(), self.get_pie(), self.get_table())
        page.render('{}/temporary2.html'.format(settings['static_path']))
        page_html = Page.save_resize_html(
            '{}/temporary2.html'.format(settings['static_path']),
            cfg_file='{}/json/world_config.json'.format(
                settings['static_path']),
            dest='{}/疫情可视化.html'.format(settings['static_path']))
        return page_html
