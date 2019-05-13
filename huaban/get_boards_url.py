# coding:utf-8
# author: gaozhengjie
# E-mail: gaozhengj@foxmail.com
# Home: https://www.gaozhengjie.cn/
# Desc: Save the urls of id (category directory)  of a user in huaban.com to the local urls.txt file.

import requests
import json

# The header is very important and interesting, so be sure to set it up, otherwise you won't get what you want.
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
	    		'accept': '*/*',
	    		'cookie':'_uab_collina=155757332922427333827892; sid=8rdXlP7boQ0UouNPum0Wrq9YtqB.tuHW4kTKV%2BaD%2B1Xvn82ubiIaSiJMWJWfCcZRJtaQUlY; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2uhgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1366.768.24; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543=1557573215; UM_distinctid=16aa699246245a-0ae9968fda6da2-5a442916-100200-16aa69924636a9; __auc=661f053016aa699274d8cb53e0a; __asc=1d94eed716aa7143ffd3169df19; CNZZDATA1256903590=1618668537-1557570594-%7C1557581395; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1557582065027; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1557582064',
	    		'accept-encoding':'gzip',
	    		'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
	    		'referer':'https://huaban.com/qe43fqwuht/',
                'Content-Type':'application/json; charset=utf-8',
           'X-Request':'JSON',
        'X-Requested-With':'XMLHttpRequest'
	    }
# Unfortunately, I didn't find the rules inside. This is the URL I manually filtered.
# I will improve it if there is a chance.
# qe43fqwuht is the id of the user who I want to crwal.
url_list = [
    'https://huaban.com/qe43fqwuht/',
    'https://huaban.com/qe43fqwuht/?jvjjofqw&limit=10&wfl=1&max=30595361',
    'https://huaban.com/qe43fqwuht/?jvjjofqx&limit=10&wfl=1&max=32147297',
    'https://huaban.com/qe43fqwuht/?jvjjofqy&limit=10&wfl=1&max=18879356',
    'https://huaban.com/qe43fqwuht/?jvjjofqz&limit=10&wfl=1&max=34344656',
    'https://huaban.com/qe43fqwuht/?jvjjofr0&limit=10&wfl=1&max=38524174',
    'https://huaban.com/qe43fqwuht/?jvjjofr1&limit=10&wfl=1&max=18177330',
    'https://huaban.com/qe43fqwuht/?jvjjofr2&limit=10&wfl=1&max=39828976',
    'https://huaban.com/qe43fqwuht/?jvjjofr3&limit=10&wfl=1&max=42824839',
    'https://huaban.com/qe43fqwuht/?jvjjofr4&limit=10&wfl=1&max=51987919'
]

board_id_list = []
for each_page in url_list:
    res = requests.get(each_page, headers=headers)
    for each_id in json.loads(res.text)['user']['boards']:
        print(each_id['board_id'], each_id['title'])
        board_id_list.append(each_id['board_id'])

with open('urls.txt', 'w', encoding='utf-8') as fp:
    for i in board_id_list:
        fp.write('https://huaban.com/boards/' + str(i) + '/\n')

with open('urls.txt', 'r', encoding='utf-8') as fp:
    urls = fp.readlines()