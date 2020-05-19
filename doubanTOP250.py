import re
import xlwt
import urllib.request
import urllib.error
from bs4 import BeautifulSoup



def main():
    DouBanTOP250url = 'https://movie.douban.com/top250?start='
    movielist = getData(DouBanTOP250url)
    savepath = r'C:\Users\PC\Desktop\电影top250.xls'
    saveData(movielist,savepath)



#正则表达式规则
findTitle = re.compile(r'<span class="title">(.*?)</span>',re.S) #电影名称
findOther = re.compile(r'<span class="other">(.*)</span>\n</a>',re.S) # 其他名称
findFtitle = re.compile(r'<span class="title">(.*?)</span>',re.S)  #外文名称
findBd1 = re.compile(r'<p class="">(.*?)<br/>',re.S)  #导演
findBd2 = re.compile(r'<br/>(.*?)</p>',re.S)  #年代类型
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>') #评分
findCount = re.compile(r'<span>(.*?)</span>',re.S)  #评分人数
findInq = re.compile(r'<span class="inq">(.*)</span>',re.S) #简介


#获取数据
def getData(DouBanTOP250url):
    movielist = []
    for i in range(0,10):
        url = DouBanTOP250url + str(i*25)   #for循环爬取10页数据
        html = askDoubanURL(url)
        soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('div',class_='item'):
            data = []
            item = str(item)

            title = re.findall(findTitle,item)[0]
            data.append(title)

            Ftitle = re.findall(findFtitle,item)[0]
            if (len(Ftitle) == 0):
                data.append(' ')
            else:
                data.append(Ftitle)

            other = re.findall(findOther,item)[0]
            other = "".join(other.split())
            other.strip()
            other = other.replace('\n','')

            data.append(other)

            bd1 = re.findall(findBd1,item)[0]
            #bd1 = re.sub("/",'',bd1)
            bd1 = "".join(bd1.split())
            bd1.strip()
            #bd1 = bd1.replace(' ','')
            #bd1 = bd1.replace('\n','')
            data.append(bd1)

            bd2 = re.findall(findBd2, item)[0]
            bd2 = "".join(bd2.split())  #去除&nbsp;
            #bd2 = re.sub("/", '', bd2)
            bd2.strip()
            #bd2 = bd2.replace(' ', '')
            #bd2 = bd2.replace('\n', '')


            data.append(bd2)

            rating = re.findall(findRating,item)[0]
            data.append(rating)

            count = re.findall(findCount,item)[0]
            count = count.replace("人评价","")  #清除 ‘人评价” 取数字
            data.append(count)

            inq = re.findall(findInq,item)
            if len(inq) !=0:
                inq = inq[0]
                data.append(inq)
            else:
                data.append('暂无简介')


            movielist.append(data)   #将数据添加到movielist 里
    print(movielist)
    return movielist

#访问网页

def askDoubanURL(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    req = urllib.request.Request(url,headers=header)
    html = ''
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html

#保存数据
def saveData(movielist, savepath):
    print('...保存中...')
    movie = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = movie.add_sheet('豆瓣电影TOP250',cell_overwrite_ok=True)
    col = ('电影名称','外文名称','其他名称','导演主演','年代类型','评分','评分人数','简介')
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d部电影"%(i+1))
        data = movielist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    movie.save(savepath)

if __name__ == "__main__":
    main()
    print('...爬取完成。。。')




