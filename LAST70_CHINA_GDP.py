#-*- codeing = utf-8 -*-   
#@time : 2020-05-02 13:46
#@Author : 朱璠
#@file : GDP.py
#@software: PyCharm

import requests
import pandas as pd
import json

GDP_EXCEL_PATH = 'china_gdp.xlsx'

def China_GDP():
    dfwds='[{"wdcode": "zb", "valuecode": "A0201"},{"wdcode":"sj","valuecode":"LAST80"}]'
    url = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgnd&rowcode=zb&colcode=sj&wds=[]&dfwds={}'
    GDP_dict = {}
    response = requests.get(url.format(dfwds))
    get_gdp_info(GDP_dict,response.json())
    save_excel(GDP_dict)
    return GDP_dict

def get_gdp_info(GDP_dict,json_obj):
    datanodes = json_obj['returndata']['datanodes']
    for node in datanodes:
        year = node['code'][-4:]
        data = node['data']['data']
        if year in GDP_dict.keys():
            GDP_dict[year].append(data)
        else:
            GDP_dict[year] = [int(year),data]
    return  GDP_dict

def save_excel(GDP_dict):
    df = pd.DataFrame(GDP_dict).T[::-1]
    df.columns =['年份','国民总收入(亿元)','国内生产总值(亿元)','第一产业增加值(亿元)','第二产业增加值(亿元)','第三产业增加值(亿元)','人均国内生产总值(元)']
    writer = pd.ExcelWriter(GDP_EXCEL_PATH)
    df.to_excel(excel_writer=writer,index=False,encoding='utf-8',sheet_name='中国70年GDP数据')
    writer.save()
    writer.close()
if __name__ == '__main__':
    result_dict = China_GDP()

import pyecharts.options as opts
from pyecharts.charts import Line, Bar, Page, Pie
from pyecharts.commons.utils import JsCode

GDP_EXCEL_PATH = 'china_gdp.xlsx'

data = pd.read_excel(GDP_EXCEL_PATH)
# 自定义pyecharts图形背景颜色js
background_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#FFFFFF'}, {offset: 1, color: '#FFFFFF'}], false)"
)

def gdp_total():
    x = data['年份']
    y = data['国内生产总值(亿元)']
    line = (Line()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(y_axis=y,
                       is_smooth=True,
                       series_name='GDP',
                       symbol_size=5,
                       is_symbol_show=True,
                       symbol="circle",
                       linestyle_opts=opts.LineStyleOpts(color="black"),
                       label_opts=opts.LabelOpts(is_show=False),
                       itemstyle_opts=opts.ItemStyleOpts(
                           color="red",  border_width=1
                       )
                       )
            .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"),
                             title_opts=opts.TitleOpts(title="中国大陆历年GDP",subtitle='单位：亿人民币'))



            .render('gdp_total.html')
                             )

if __name__ == '__main__':
    gdp_total()
