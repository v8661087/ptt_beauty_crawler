import requests
from bs4 import BeautifulSoup
import os

# 
url = 'https://www.ptt.cc/bbs/Beauty/M.1548306249.A.115.html'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

title_all =soup.select("span.article-meta-value")
title = title_all[2].text
print(title)
for r_ent in soup.find_all('a', rel='nofollow'):
  img = r_ent['href']
  if img.endswith('jpg') or img.endswith('png') or img.endswith('jpeg'):
      rs = requests.session()
      res_img = rs.get(img, stream=True)
      image_name = img.split('/')[-1]
      folder_path = ""+ title +'/'
      if not os.path.exists(folder_path):        #如果沒有資料夾，自動創建
        os.makedirs(folder_path)
      with open(folder_path+'%s' % image_name, 'wb') as f:
        f.write(res_img.content)
        print('Saved %s' % image_name)