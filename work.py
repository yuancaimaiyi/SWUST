'''************爬取西南科大官网上的工作*************'''
import requests
import xlwt
import bs4
from bs4 import  BeautifulSoup
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
def gethtml(url,headers):
    r=requests.get(url,headers=headers)
    return r
def bs4parser(html):
    soup=BeautifulSoup(html,'html.parser')
    return soup
if __name__=='__main__':
    work=[]
    page=50
    i=1
    while i<=page:
        url=r'http://job.swust.edu.cn/l_QYservice.aspx?pd=171&cpd=1&pn=&v=%c6%f3%d2%b5%b7%fe%ce%f1&page='+str(i)
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}
        r=gethtml(url,headers=headers)
        r.encoding=r.apparent_encoding
        s1=bs4parser(r.text)
        for a in s1.find(class_='rcont').find_all('a'):#用属性值来过滤，避免有其他ul标签
            if isinstance(a,bs4.element.Tag):
                for span in a('span'):
                    work.append(span.string)
        i+=1
#        li=s1.find_all('ul')#当初的笨办法，用ul标签过滤的，结果不曾想到有好几个ul标签'''
#        for a in li[3].find_all('a'):
#            if isinstance(a,bs4.element.Tag):
#                for span in a('span'):
#                    work.append(span.string)
#        i+=1
''' 用excel 保存爬取的工作'''
book=xlwt.Workbook()
sheet = book.add_sheet('工作')
if len(work)%4 !=0:
    row= int((len(work)-(len(work)%4))/4)
else:
    row=int(len(work)/4)
sheet.write(0, 0,'招聘日期')
sheet.write(0, 1,'发布日期')
sheet.write(0, 2,'招聘公司')
sheet.write(0, 3,'招聘职位')
for i in range(1,row+1):
    sheet.write(i,0,work[(i-1)*4])
    sheet.write(i,1,work[(i-1)*4+1])
    sheet.write(i,2,work[(i-1)*4+2])
    sheet.write(i,3,work[(i-1)*4+3])
book.save(r'C:\Users\Y\Desktop\work.xls')
'''*********统计前1000家公司的招聘月份分布********'''
years=[]
months=[]
r1=r'\d{4}'
r2=r'-(\d{2})'
for i in range(len(work)):
    if i%4==0:
        years.append(re.findall(r1,work[i])[0])
        months.append(re.findall(r2,work[i])[0])
index1=[i for i in range(len(years)) if years[i]=='2016']
index2=[i for i in range(len(years)) if years[i]=='2015']
total_year=Counter(years)
if index1 !=[]:
    t17=Counter(months[:index1[0]])
    t16=Counter(months[index1[0]:index2[0]])
else:
    t17=Counter(months[:])
    t16=Counter([])
def monthCounter(n1):
    num=[]
    for i in range(1,13):
        if i<10:
            num.append(n1['0'+str(i)])
        else:
            num.append(n1[str(i)])
    return num
n17=monthCounter(t17)
n16=monthCounter(t16)
plt.bar(np.arange(12),n17,0.5,color='r')
plt.bar(np.arange(12)+0.4,n16,0.5,color='y')
plt.xticks(np.arange(12)+0.4,('1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'),fontproperties='FangSong',fontsize=14)
plt.ylabel('公司个数',fontproperties='FangSong',fontsize=14)
plt.title('爬取1000家公司，2016-2017年总%s家\n2017年宣讲会%s家(红色),2016年宣讲会%s家(黄色)'%(total_year['2017']+total_year['2016'],total_year['2017'],total_year['2016']),fontproperties='FangSong',fontsize=14)      
plt.show()
    

