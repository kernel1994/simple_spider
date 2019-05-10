# coding:utf-8
# author: gaozhengjie
# E-mail: gaozhengj@foxmail.com
# Home: https://www.gaozhengjie.cn/
# Desc: Get comments for a specific item and save into a excel file.

import requests
import json
import time
import random
import openpyxl
import os


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


def main(first_url, url_left, callback, url_right):
	result = []
	for i in range(100):  # 10 per page, so a total of 100 pages
	    if i==0:
	    	baseurl = first_url
	    else:
	    	baseurl = url_left + str(i) + url_right
	    print(baseurl)
	    print("-----------------------------------------------------------------------------------")
	    headers = {'user-agent':USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)],
	    		'accept': '*/*',
	    		'cookie':'shshshfpa=853e6b28-c80f-b8a7-dd64-0be6a8361711-1535810943; shshshfpb=2b543b5b5c680451eb658d395ffea1ba75b0d7304a039c27acd8a9d801; pinId=JmsWo3Oi-C46kev099xv8LV9-x-f3wj7; TrackID=1QTMFSrS5AwDS-GnIF1HDv2hmbNFEzfRbcrL2b_k2ookvjiC5jXrO4U9_neHFnyyJz6GLR6o1ThMcIGGGk-NOLCb1YdSC6g2cwpVaCDGegaw; __jdu=15358109413918115072; unpl=V2_ZzNtbUsFRxcgDEUDL0kJV2IHE1gRVEQdcgwWUXsaDAA3BUUJclRCFX0UR1BnGV0UZAMZXkBcQxVFCEZkexhdBGADFV5CVnMldDhFVEsRbAVjARZUQlZLEHUKTlRyGVwBZgURbXJQcyUtUxYJLFtsBFcCIl1yHC0UOAhCVn8QXARvBhJfSldKFXUMR1J4KV01ZA%3d%3d; __jda=122270672.15358109413918115072.1535810941.1547461228.1557494592.26; __jdc=122270672; __jdv=122270672|kong|t_1000616210_|tuiguang|8c53d52feadc4504b26965a412a4a7fe|1557494591853; areaId=22; PCSYCityID=1930; JSESSIONID=51AF1094192B48B8DABE4C19A027E03E.s1; ipLoc-djd=1-72-2799-0; 3AB9D23F7A4B3C9B=CUBSYVUSULJLSQ6XBRVPVA2VMJZ2P7Y6XI5USHNNU7Y2XAZGNR267DOUAV6XDL5D5CDHZTMTMVPTPQRKM7BO5UHXZE; shshshfp=2960c0012d594bc0ed250f799332c639; shshshsID=da5aa8571d514cdf5a802e61c10635e6_5_1557495929998; __jdb=122270672.8.15358109413918115072|26.1557494592',
	    		'accept-encoding':'gzip, deflate, br',
	    		'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
	    		'referer':'https://item.jd.com/7694047.html'
	    }
	    res = requests.get(baseurl, headers=headers, verify=False)  # Free verification
	    dic = json.loads(res.text[len(callback)+1:-2])
	    for i in dic['comments']:
	        result.append(i['content'])
	    sleep_time=random.randint(1, 3)  # Random sleep program to prevent being blocked
	    time.sleep(sleep_time)
	return result


def save_excel(data, filename):
	wbk = openpyxl.Workbook()  # Create a new workbook
	sheet = wbk.active  # Get a running worksheet
	for each_comment in data:
	    sheet.append([each_comment])
	wbk.save(filename)


if __name__ == '__main__':
	url_right = '&pageSize=10&isShadowSku=0&rid=0&fold=1'
	
	callback = 'fetchJSON_comment98vv883'  # you can find these information via Chrome console.
	productId = '7694047'  # The id of item is unique.
	url_left = 'https://sclub.jd.com/comment/productPageComments.action?callback=' + callback + '&productId=' + productId + '&score=0&sortType=5&page='
	first_page_url = url_left + '0&pageSize=10&isShadowSku=0&fold=1'
	result = main(first_url=first_page_url, url_left=url_left, callback=callback, url_right=url_right)
	save_excel(data=result, filename="honor_9i_jd_7694047.xlsx")