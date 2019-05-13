#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This code get from https://github.com/luoyi2017/huaban_spider
# I just made very minor changes to the code. That is 23 line to 29 line.

import requests,re,time,os,random,multiprocessing
import urllib.request as request
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}

params = {
    'max': '',
    'limit': '20'
}

# 填入待下载画板（不限画板数量），多进程下载（CPU有几个内核就调用几个进程），1个画板调用1个进程。
# urls = [
#     'https://huaban.com/boards/24885662/',
#     'https://huaban.com/boards/29471563/',
# ]
with open('urls.txt', 'r', encoding='utf-8') as fp:
    urls = [x.strip() for x in fp.readlines()]

# 设置下载目录
directory = "F:huaban\img\\"

# 通过画板url获取图片真实地址，例url = 'http://huaban.com/boards/38677770/'
def get_links(url):
    # print('get_links1',type(url),url)
    # 将初始max设置为空，否则调用多进程下载下一个画板时沿用上一次的max值，导致获取不准确。
    params['max']=''
    r = requests.get(url, params=params, headers=headers)
    # print('get_links2', r.json()['board']['pins'])
    if '/boards' in url:
        # print('get_links3', r.json())
        board_id = r.json()['board']['board_id']
        title = r.json()['board']['title']
        img_addrs = []
        # img_dict用于将图片链接和图片id绑定起来
        img_dict = {}
        # print('get_links4')
        last_pin_id = str(r.json()['board']['pins'][-1]['pin_id'])
        # print('get_links5',last_pin_id)
        for i in r.json()['board']['pins']:
            img_addrs.append('//img.hb.aicdn.com/' + i['file']['key'])
            img_dict[i['file']['key']] = i['pin_id']
        # print('get_links6',type(img_dict),img_dict)
        # 调用下载
        while True:
            # 可考虑加个网址判断
            new_url = url + '?max=' + last_pin_id + '&limit=20&wfl=1'
            # print('get_links7', new_url)
            try:
                params['max'] = last_pin_id
                r = requests.get(new_url, params=params, headers=headers)
                for i in r.json()['board']['pins']:
                    # print('http://huaban.com/pins/%s/' % i['pin_id'])
                    img_addrs.append('//img.hb.aicdn.com/' + i['file']['key'])
                    img_dict[i['file']['key']] = i['pin_id']
                last_pin_id = str(r.json()['board']['pins'][-1]['pin_id'])
                # print('get_links8', last_pin_id)
            except:
                break
        # img_addrs = list(set(img_addrs))，实现去重，但是发现没有重复的，所有可以不用去重
        print('进程号:'+str(os.getpid())+'；'+'画板id:'+str(board_id)+'；'+'画板名称:' + str(title)+'；'+'图片数量:' + str(len(img_addrs))+'-----开始下载！')
        # 给文件夹取名
        filename = title + '(' + str(len(img_addrs)) + '图)' + '_' + str(board_id)
        # print('get_links9', filename，img_addrs)
        time.sleep(3)
        # print('get_links10')
        return (filename, img_addrs, img_dict)
    else:
        print('请使用画板链接，即URL地址包含关键词boards')
        pass
# get_links(url)

def save_imgs(img_addrs, img_dict):
    # print('save1')
    down_list = []
    nodown_list = []
    for img_link in img_addrs:
        # print('save2')
        img_name = str(img_dict[img_link.split('/')[-1]]) + '.jpg'
        # urlretrieve() 将远程数据下载到本地。urlretrieve(url, filename=None, reporthook=None, data=None)
        # finename 指定了保存本地路径， reporthook 是一个回调函数，可利用来显示当前的下载进度。
        img_link_http = 'http:'+ img_link
        request.urlretrieve(img_link_http, img_name)
        # print('save3')
        down_list.append(img_link)
        # print('save4')
        # if len(img_addrs)%100 == 0:
        #     time.sleep(random.random()*1 + 1)
        # if TimeoutError:
        #     print('连接方没有回应，保存进度！')
        #     break
        nodown_list = list(set(img_addrs) - set(down_list))
    if nodown_list == []:
        print('进程号:'+str(os.getpid())+'-----下载完成！')
    return(nodown_list)
# save_imgs(['//img.hb.aicdn.com/2af3c2a5ca8ddd99fe20114bbdb35a4336367995308e9-Uce7ty','//img.hb.aicdn.com/9410d96fee974984b0b18c81b7f0d94a589448d519297-HQQAjL'])

def save_nodown(nodown_list):
    # print('nodown1')
    if len(nodown_list) > 0:
        # print('nodown2')
        with open('nodown.txt', 'a+') as f:
            f.write(str(nodown_list))
    else:
        pass

# 主程序：
def file(url):
    # print('file1',url)
    now_folder = os.getcwd()
    get_links_r = list(get_links(url))
    # print('aaa',get_pins_r)
    filename = get_links_r[0]
    # 判断folder文件夹是否存在，不存在则创建，并保存图片
    if os.path.exists(directory + filename) == 1:
        print('文件夹已存在')
        pass
    else:
        # 创建文件夹
        os.mkdir(directory + filename)
        # 切换到新创建的文件夹内
        os.chdir(directory + filename)
        img_addrs = get_links_r[1]
        # print('aaa',type(img_addrs),img_addrs)
        # print('file2')
        # 下载图片
        img_dict = get_links_r[2]
        nodown_list = save_imgs(img_addrs, img_dict)
        # print('file3')
        save = save_nodown(nodown_list)
        # 切换回py文件当前路径
        os.chdir(now_folder)
        # print('file4')
# file(url)

if __name__ == '__main__':
    start = time.time()
    # print('start', start)
    pool = multiprocessing.Pool(8)
    n = 0
    for i in range(len(urls)+1):
        url = urls[n]
        # print('main1',url)
        pool.apply_async(file, (url,))
        n += 1
        # print('main2',n)
        if n == len(urls):
            # print('main3')
            break
    # print('zzzzz')
    pool.close()
    pool.join()
    end = time.time()
    # print('end', end)
    print('所用时间：', str(end - start), '秒')
