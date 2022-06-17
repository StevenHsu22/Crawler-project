import json
import requests
import time
import sys, urllib
from bs4 import BeautifulSoup
from bs4.element import NavigableString


root = "https://www.ptt.cc/bbs/"
main = "https://www.ptt.cc"
gossip_data = {
        "from":"bbs/Gossiping/index.html",
        "yes": "yes"
    }

rs = requests.session()

# 爬文章網址
def articles(page):
    requests.packages.urllib3.disable_warnings()
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=gossip_data)
    res  = rs.get(page)
    soup = BeautifulSoup(res.text, "lxml")

    for article in soup.select(".r-ent"):
        if article.select(".title")[0].select("a")[0].get("href") != '/bbs/Food/M.1599055881.A.3C7.html':
            try:
                yield main + article.select(".title")[0].select("a")[0].get("href")
            except:
                pass # (本文已被刪除)

# 轉換時間格式
def timechange(day):
    timeString = day
    struct_time = time.strptime(timeString, "%a %b %d %H:%M:%S %Y")
    new_timeString = time.strftime("%Y-%m-%d", struct_time)
    return new_timeString

# 轉換推文的時間
def timechange_push(year, day):
    day_c = day.replace('\n', '')
    timeString = year + day_c.replace(' ', '')
    struct_time = time.strptime(timeString, "%Y%m/%d%H:%M")
    new_timeString = time.strftime("%Y-%m-%d", struct_time)
    return new_timeString

# 爬內文    
def parse_article(url, board = 'Food', corp = '王品集團', Brand = "饗饗"):       
    raw  = rs.get(url)
    soup = BeautifulSoup(raw.text, "lxml")

    try:
        article = {}
    
        # 取得文章作者與文章標題
        article["Corp"]   = corp
        article["Brand"]  = Brand
        article["Platform"]  = "Ptt"
        article["Branch"]  = ""
        article["Username"] = soup.select(".article-meta-value")[0].contents[0].split(" ")[0]
        article["ReviewTime"]   = timechange(soup.select(".article-meta-value")[3].contents[0])
        article["Title"]  = soup.select(".article-meta-value")[2].contents[0]
        
        # 取得內文
        content = ""
        for t in soup.select("#main-content")[0]:
            if type(t) is NavigableString and t !='\n':
                content += t
                break
        article["ReviewContent"] = content
        article["ReviewStar"] = ""
        article["commentCount"] = ""
        
        # 處理回文資訊
        
        year = soup.select(".article-meta-value")[3].contents[0][-4:]
        article_response_list = []
        
        for response_struct in soup.select(".push"):
            # 跳脫「檔案過大！部分文章無法顯示」
            if "warning-box" not in response_struct['class']:

                article_response = {}
                article_response["Corp"]   = corp
                article_response["Brand"]  = Brand
                article_response["Platform"]  = "Ptt"
                article_response["Branch"]  = ""
                article_response["Username"] = response_struct.select(".push-userid")[0].contents[0] 
                if board != 'Gossiping':
                    article_response["ReviewTime"] = timechange_push(year, response_struct.select(".push-ipdatetime")[0].contents[0])
                else:
                    article_response["ReviewTime"] = timechange_push(year, response_struct.select(".push-ipdatetime")[0].contents[0][-13:])
                article_response["Title"]  = soup.select(".article-meta-value")[2].contents[0]
                article_response["ReviewContent"]= response_struct.select(".push-content")[0].contents[0][1:]
                article_response["ReviewStar"] = ""
                article_response["commentCount"] = ""
                article_response_list.append(article_response)
                
    except Exception as e:
        print(e)
        print(u"在分析 %s 時出現錯誤" % url)
        
    final_art = [article]
    
    for i in article_response_list:
        final_art.append(i)
   
    return final_art

def output(filename, data):
    try:
        with open(filename +".json", 'wb+') as f:
            f.write(json.dumps(data, indent=1, ensure_ascii=False).encode('utf-8'))
            print('爬取完成', filename + '.json', '輸出成功')
    except Exception as err:
        print(filename +'.json', '輸出失敗')
        print('error message:', err)

def ptt_crawler(board = 'Gossiping', corp = '王品集團', search = '%E7%8E%8B%E5%93%81', start_page = 1, end_page = 2):
    res = []
    for j in range(start_page, end_page+1):
        url = 'https://www.ptt.cc/bbs/'+ board + '/search?page='+ str(j) + '&q=' + search
        for i in articles(url):
            res.extend(parse_article(i, board = board, corp = corp, Brand = search))
            time.sleep(1)   
        print(u"已經完成 %s 頁面第 %d 頁的爬取" %(board, j))

    output('ptt_'+ board+ '_'+ search, res) 

 if __name__ == '__main__':
    #輸入要爬取的看板、關鍵字與頁數
    ptt_crawler(board = 'Gossiping', corp = '饗賓集團', search = '開飯川', start_page = 1, end_page = 1)
