from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import json

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
	'Host':'m.weibo.cn',
	'Referer':'https://m.weibo.cn/u/2145291155',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest',
}

def get_page(page):
	params = {
		'type':'uid',
		'value':'2145291155',
		'containerid':'1076032145291155',
		'page':page
	}
	url = base_url + urlencode(params)
	try:
		response = requests.get(url,headers=headers)
		if response.status_code == 200:
			return response.json()
		else:
			print(response.status_code)
	except requests.ConnectionError as e:
		print('Error', e.args)

def parse_page(json):
	if json:
		items = json.get('data').get('cards')
		for item in items:
			item = item.get('mblog')
			weibo = {}
			weibo['id'] = item.get('id')
			weibo['text'] = pq(item.get('text')).text()
			weibo['attitudes'] = item.get('attitudes_count')
			weibo['comments'] = item.get('comments_count')
			yield weibo
def main():
	for page in range(1,15):
		json1 = get_page(page)
		results = parse_page(json1)
		for result in results:
			print(result)
			with open('weibo.txt','a',encoding='utf-8')as f:
				#a = 'aaaaaaa'
				text = json.dumps(result,indent=2,ensure_ascii=False)
				f.write(text)
				f.write('\n')
main()
