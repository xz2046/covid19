import pandas as pd
import datetime
from pyecharts.charts import Map, Line, Calendar, Bar, Pie, Page
import pyecharts.options as opts
from pyecharts.components import Table

from app.settings import engine, settings

pieces = [{
    'value': 0,
    'color': '#F5F5F5'
}, {
    'min': 1,
    'max': 9
}, {
    'min': 10,
    'max': 99
}, {
    'min': 100,
    'max': 499
}, {
    'min': 500,
    'max': 999
}, {
    'min': 1000,
    'max': 9999
}, {
    'min': 10000,
    'lable': '1000人及以上'
}]
color = [
    '#D87C7C', '#919E8B', '#D7AB82', '#6E7074', '#61A0A8', '#EFA18D',
    '#787464', '#CC7E63', '#724E58', '#4B565B', '#D87C7C', '#919E8B',
    '#D7AB82', '#6E7074', '#61A0A8'
]


class GetChart():
    def __init__(self) -> None:
        #engine = create_engine("mysql+pymysql://root:********@localhost:3306/databasename?charset=utf8")
        self.df_today = pd.read_sql('select * from ctoday;', engine)
        self.df_sum = pd.read_sql('select * from cdatas;',
                                  engine).set_index('日期')
        self.df_all = pd.read_sql('select * from ctodays;', engine)

        times = datetime.datetime.now()
        self.today = times.date()

    def get_map(self):
        df_map = self.df_today
        map_chart = (Map(init_opts=opts.InitOpts(chart_id='01001')).add(
            '累计确诊',
            list(zip(df_map['省份'], df_map['累计确诊'])),
            'china',
            is_roam=False,
            max_scale_limit=1.5,
            min_scale_limit=0.8,
            is_map_symbol_show=False).set_global_opts(
                title_opts=opts.TitleOpts(
                    title="疫情实时追踪平台",
                    pos_left='center',
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_weight='bold', font_size=36, font_family='华文楷体')),
                legend_opts=opts.LegendOpts(selected_mode='single',
                                            pos_bottom='bottom',
                                            is_show=False),
                visualmap_opts=opts.VisualMapOpts(max_=70000,
                                                  is_piecewise=True,
                                                  pieces=pieces),
            ))
        return map_chart

    def get_line(self):
        df_line = self.df_sum.sort_index()
        line_chart = (Line(init_opts=opts.InitOpts(
            chart_id='01002')).add_xaxis(df_line.index.tolist()).add_yaxis(
                '累计确诊', df_line['累计确诊'].tolist()).add_yaxis(
                    '累计死亡', df_line['死亡'].tolist()).add_yaxis(
                        '累计治愈', df_line['治愈'].tolist()).set_global_opts(
                            xaxis_opts=opts.AxisOpts(
                                axislabel_opts=opts.LabelOpts(
                                    font_weight='bold')),
                            yaxis_opts=opts.AxisOpts(
                                axislabel_opts=opts.LabelOpts(
                                    font_weight='bold')),
                            datazoom_opts=opts.DataZoomOpts(is_show=True,
                                                            range_start=0,
                                                            range_end=50)))
        return line_chart

    def get_calendar(self):
        date = pd.date_range('2020-01-19', self.today).to_series()
        df_cale = pd.concat([date, self.df_sum], axis=1).fillna(method='pad')
        data = list(zip(df_cale.index.tolist(), df_cale['现有病例'].tolist()))
        cale_chart = (Calendar(init_opts=opts.InitOpts(chart_id='01003')).add(
            '存在确诊',
            yaxis_data=data,           
            calendar_opts=opts.CalendarOpts(
                range_=['2020-01-19', self.today],
                pos_top="120",
                pos_left="30",
                daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
                monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn"),
                pos_right="30")).set_global_opts(
                    visualmap_opts=opts.VisualMapOpts(max_=5000,
                                                      orient='horizontal',
                                                      is_piecewise=False),
                    legend_opts=opts.LegendOpts(is_show=False),
                    title_opts=opts.TitleOpts(title='每日确诊日历图',
                                              pos_left='center',
                                              pos_bottom='bottom')))
        return cale_chart

    def get_bar(self):
        df_bar = self.df_today.sort_values(by=['新增', '累计确诊'],
                                           ascending=False).head(6)
        bar_chart = (Bar(init_opts=opts.InitOpts(chart_id='01004')).add_xaxis(
            df_bar['省份'].tolist()).add_yaxis(
                '新增病例', df_bar['新增'].tolist(),
                color='#CD0000').set_global_opts(
                    legend_opts=opts.LegendOpts(selected_mode='single',
                                                is_show=False),
                    title_opts=opts.TitleOpts(title='今日新增确诊省份TOP6',
                                              pos_left='center',
                                              pos_bottom='bottom')))
        return bar_chart

    def get_pie(self):
        df_pie = self.df_today
        pie = (Pie(init_opts=opts.InitOpts(chart_id='01005')).add(
            '',
            list(zip(df_pie['省份'], df_pie['现有病例'])),
            radius=['35%', '65%'],
            label_opts=opts.LabelOpts(is_show=False)).set_colors(
                colors=color).set_global_opts(
                    legend_opts=opts.LegendOpts(is_show=False),
                    title_opts=opts.TitleOpts(title='现有病例',
                                              pos_left=20,
                                              pos_top=20)))
        return pie

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
                'font-size: 140%;color:#363636;text-align:center;font-family:宋体;font-weight:bold;'
            })
        return table_chart

    def run(self):
        page = Page()
        page.add(self.get_bar(), self.get_calendar(), self.get_line(),
                 self.get_map(), self.get_pie(), self.get_table())
        page.render('{}/temporary.html'.format(settings['static_path']))
        page_html = Page.save_resize_html(
            '{}/temporary.html'.format(settings['static_path']),
            cfg_file='{}/json/china_config.json'.format(
                settings['static_path']),
            dest='{}/疫情可视化.html'.format(settings['static_path']))
        return page_html
