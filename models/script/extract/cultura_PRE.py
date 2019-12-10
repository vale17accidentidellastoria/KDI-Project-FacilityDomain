import json
import requests


def rm_main():
	url = 'https://raw.githubusercontent.com/vale17accidentidellastoria/KDI-Project-FacilityDomain/master/data/cultura.json'
	obj = json.loads(requests.get(url).text)
	return json.dumps(obj)
