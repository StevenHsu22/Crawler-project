from requests import session
import time
import random
import json
from fake_useragent import UserAgent


#搜尋文章
def search_article(corp = '王品', brand = '饗泰多'):
    
    ua = UserAgent(use_cache_server=False)
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    s = session()
    
    api = 'https://www.dcard.tw/service/api/v2'
    url = api + '/search/posts?query='+ brand

    res = s.get(url, headers = headers)
    html = res.text
    rejs = json.loads(html)

    final_art = []
    #存取文章
    for i in rejs:
        try:
            a = {}
            a['Corp'] = corp
            a['Brand'] = brand
            a['Platform'] = "Dcard"
            a['Branch'] = ""
            a['Username'] = i['memberId']
            a['ReviewTime'] = i['createdAt'][0:10]
            a['Title'] = i['title']
            a['ReviewContent'] = i['excerpt']
            a['ReviewStar'] = ""
            a['commentCount'] = i['commentCount']
            final_art.append(a)

            #爬回文資訊
            url2 = api+ '/posts/'+ str(i['id']) + '/comments'
            res2 = s.get(url2, headers = headers)
            html2 = res2.text
            CmntsData = json.loads(html2)

            comment_content = []
            print('正在爬這篇文章', i['title'])
            time.sleep(random.randint(1,3))
            for j in CmntsData:
                try:
                    b = {}
                    b['Corp'] = corp
                    b['Brand'] = brand
                    b['Platform'] = "Dcard"
                    b['Branch'] = ""
                    b['Username'] = j['id']
                    b['ReviewTime'] = j['createdAt'][0:10]
                    b['Title'] = i['title']
                    b['ReviewContent'] = j['content']
                    b['ReviewStar'] = ""
                    b['commentCount'] = ""
                    comment_content.append(b)
                    print('正爬到第', j['floor'], '樓')
                    time.sleep(random.randint(1,3))
                except KeyError:
                    print('留言被刪除')
                    continue

            for i in comment_content:
                final_art.append(i)
                    
        except Exception as err:
            print(err)
            continue
            
    return final_art

#輸出成json檔
def output(filename, data):
    try:
        with open(filename +".json", 'wb+') as f:
            f.write(json.dumps(data, indent=1, ensure_ascii=False).encode('utf-8'))
            print('爬取完成', filename + '.json', '輸出成功')
    except Exception as err:
        print(filename +'.json', '輸出失敗')
        print('error message:', err)

if __name__ == '__main__':
    #輸入要爬的關鍵字
    data = search_article(corp = '王品集團', brand = '原燒')
    output("原燒", data)
