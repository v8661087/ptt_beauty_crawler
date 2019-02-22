import os
import requests
from bs4 import BeautifulSoup

push_rate = 90 #調整大於的推數
url = "https://www.ptt.cc/bbs/Beauty/index.html" #網址
for i in range(10):  #頁數
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            articleurl = r_ent.find('a')['href']    #每篇文章的網址
        except TypeError:                           #如果文章已被刪除會出現TypeError: 'NoneType' object is not subscriptable
            continue
        title = r_ent.find(class_="title").text.strip()
        rate_text = r_ent.find(class_="nrec").text
        author = r_ent.find(class_="author").text
              
        if rate_text:
            if rate_text.startswith('爆'):
                rate = 100
            elif rate_text.startswith('X'):
                rate = -1 * int(rate_text[1])
            else:
                rate = rate_text
        else:
            rate = 0

        if int(rate) >= push_rate and  (title.startswith('[正妹]')  or title.startswith('[新聞]')): #比對推文數
            #print(rate,"推",'https://www.ptt.cc/'+articleurl, title)
            print(rate,"推",title)                   
            url2 = 'https://www.ptt.cc/'+articleurl
            res2 = requests.get(url2)
            soup2 = BeautifulSoup(res2.text, "html.parser")
            #print(soup2)
            for r_ent2 in soup2.find_all("a", rel='nofollow'):
                #print(r_ent2)
                x = r_ent2['href']
                if x.endswith('jpg') or x.endswith('png') or x.endswith('jpeg'):
                    #print(x)
                    rs = requests.session()
                    res_img = rs.get(x, stream=True)
                    image_name = x.split('/')[-1]
                    #path = 'D:\python-training\img'
                    folder_path = "D:\python-training\img/" + str(rate)+"推" + title +"/"
                    if not os.path.exists(folder_path):        #如果沒有資料夾，自動創建
                        os.makedirs(folder_path)

                    with open(folder_path+'%s' % image_name, 'wb') as f:
                        f.write(res_img.content)
                        print('Saved %s' % image_name)
            #print("下一頁")
                    
   #print("目前網址"+url)
    u = soup.select("div.btn-group.btn-group-paging a") #上一頁按鈕的a標籤
    url = "https://www.ptt.cc"+ u[1]["href"] #上一頁的網址
       

