import requests
import json
import pandas as pd


def get_movie(url,head):
    movie_list = []
    for year in range(1983,2021): #for循环年份
        data = {'year': year, 'MethodName': 'BoxOffice_GetYearInfoData'}
        response  = requests.post(url,data=data,headers=head)  #请求网页
        response .raise_for_status()
        jsonobj = json.loads(response .text)
        movie_list += jsonobj['Data']['Table'] #添加数据
    df = pd.DataFrame(movie_list)      #创建数据框
    df.to_excel("历年电影top票房.xls")   #保存表格

def main():
    url = 'http://www.endata.com.cn/API/GetData.ashx'
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    get_movie(url,head)

if __name__ == '__main__':
    main()

