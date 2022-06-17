# Crawler 

*17 June 2022. Update: 2022/06/17.*

* [所需python套件](#env)
* [Ptt爬蟲](#pttcrawler)
* [Dcard爬蟲](#dcardcrawler)
* [Google評論爬蟲](#googlecrawler)

<h2 id="env">所需python套件</h2>

* requests

* bs4

* fake_useragent

###程式目標

* 爬取各大平台餐飲資料，並存成所需欄位，最終進行資料分析。

<h2 id="pttcrawler">Ptt爬蟲</h2>

* [pttcrawler](https://github.com/StevenHsu22/Crawler/tree/master/pttcrawler): 透過 requests 與 bs4 抓取資料，並可自行設定關鍵字與頁數。

<h2 id="dcardcrawler">Dcard爬蟲</h2>

* [dcardcrawler](https://github.com/StevenHsu22/Crawler/tree/master/dcardcrawler): 透過 Dcard API 中搜尋關鍵字的語法抓取特定資料，另特別使用 fake_useragent 避免被擋爬。

<h2 id="googlecrawler">Google評論爬蟲</h2>

* [googlecrawler](https://github.com/StevenHsu22/Crawler/tree/master/googlecrawler): 透過 requests 爬取 google 地圖的評論資料，且需在事前將須爬取店家的 requests 存成另一個檔案，此外，也特別使用 fake_useragent 避免被擋爬。

補充：店家 requests 的查找方式
1.選擇一個商家資訊網址
2.打開開發者工具 > Network > XHR。
3.重新整理，讓工具抓到新讀取的資料。
4.找到重複的連結(listentitiesreviews….)。

