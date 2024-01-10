from bs4 import BeautifulSoup
import requests
import pandas as pd
pages=200
x=[]
for i in range(50,pages):
    url="https://www.zameen.com/Homes/Karachi-2-"+str(i)+".html"
    req=requests.get(url)
    soup=BeautifulSoup(req.text,'html.parser')
    div=soup.find_all('div', class_='f74e80f3')
    for i in range(len(div)):
        link=div[i].find('a').get('href')
        string='https://www.zameen.com'
        link2=string+link
        req2=requests.get(link2)
        soup2=BeautifulSoup(req2.text,'html.parser')
        try:    
            li=soup2.find('div',class_="_208d68ae c352c124 _1aca585a").find(class_='_066bb126').find('ul').find_all('li')
        except:
            print("shit ad")
        for y in li:
            x.append(y.find_all('span')[1].get_text())
            
type_=[x[i] for i in range(0,len(x),8)]
price=[x[i] for i in range(1,len(x),8)]
location=[x[i] for i in range(2,len(x),8)]
bathroom=[x[i] for i in range(3,len(x),8)]
area=[x[i] for i in range(4,len(x),8)]
purpose=[x[i] for i in range(5,len(x),8)]
bedroom=[x[i] for i in range(6,len(x),8)]
added=[x[i] for i in range(7,len(x),8)]

df=pd.DataFrame(data={'type':type_,'price':price,'location':location,'bathroom':bathroom,'area':area,'purpose':purpose,'bedroom':bedroom,'added':added})
df.to_csv("zameen_data 1 2021.csv")