import requests
import time
import random
import json
from requests import session
from fake_useragent import UserAgent
from time_change import timechange

ua = UserAgent(use_cache_server = False)
user_agent = ua.random
headers = {'user-agent': user_agent}

s = session()

pretext = ')]}\''

with open('饗賓google.json', 'r', encoding = "utf-8") as f:
    a = json.loads(f.read())

all_content = []    
for i in a:
    flag = 0
    time.sleep(1)
    for page in range(0,3000):
        if flag != 1:
            res = s.get(i['google_url'].format(page), headers=headers)
            text = res.text.replace(pretext, '')
            soup = json.loads(text)
            conlist = soup[2]
        else:
            break
        try:
            for j in conlist:
                if j[1] != '1 年前':
                    a = {}
                    a['Corp'] = '王品集團'
                    a['Brand'] = i['品牌']
                    a['Branch'] = i['分店']
                    a['Username'] = j[0][1]
                    a['ReviewTime'] = timechange(j[1])
                    a['ReviewContent'] = j[3]
                    a['ReviewStar'] = j[4]
                    all_content.append(a)
                else:
                    flag = 1
                    break
            print(i['品牌'], i['分店'], 'now page', page)
            time.sleep(random.randint(1,3))
        except TypeError:
            print('評論較少')
            flag = 1
            break

y = json.dumps(all_content, ensure_ascii = False, indent = 1)
file_name = '饗賓_google_reviews.json'
with open(file_name , 'w', encoding = "utf-8") as f:
    f.write(y)
