# coding: utf-8
# Author: gaozhengjie
# Description: 测试代理是否可用
# 
import requests

def GetUseProxies():
	UseProxiesList = []
	i = 1
	n =0
	# 这个地方我用的是蜻蜓代理 https://proxy.horocn.com/
	# 新用户会有200个免费的IP，但不一定都能用
	# 请求api返回代理列表
	api = "https://proxy.horocn.com/api/proxies?order_id=HUY91633967379732308&num=10&format=text&line_separator=win"

	api_url = requests.get(api).text
	proxies_list= api_url.split('\r\n')
	print(proxies_list)
	print('获得proiex%s' % len(proxies_list))
	for proxy in proxies_list:
		print('正在发送第%s个请求。\n\r' % i)
		i+=1
		proxies = { "http": "http://"+proxy, "https": "http://" + proxy, }
		try:
			requests.get('http://www.baidu.com', proxies=proxies, timeout=2)
			UseProxiesList.append(proxy)
		except:
			n+=1
		print('***已经有%s个代理被淘汰***' % n)
		print('UseProxiesList:', UseProxiesList)
		print('可用代理数量%s' % len(UseProxiesList))


if __name__ == "__main__":
	GetUseProxies()