import json
import requests


def rm_main():
	url = 'https://raw.githubusercontent.com/andreamatt/KDI/master/dataset/cultura.json'
	obj = json.loads(requests.get(url).text)
	return json.dumps(obj)
