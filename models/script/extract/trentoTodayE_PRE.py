import json
import requests

fields = ['Title', 'Link', 'category', 'location', 'price', 'date', 'time', 'description', 'startDate', 'endDate', 'startTime', 'endTime']


def fill_event(e):
	for f in fields:
		e[f] = e.get(f, '').replace('\n', '; ')


utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)

cat_dict = {
    science: ['enogastronomia', 'eventi rifugi'],
    visual: ['mercati e mercatini', 'mostre', 'spettacoli pirotecnici', 'visite guidate'],
    music: ['feste e sagre', 'festival', 'fiere', 'musica'],
    screen: ['cinema'],
    theatre: ['teatro/danza', 'intrattenimento della località', 'folklore'],
    talk: ['conferenze/congressi', 'rifugi aperti'],
    general: ['altro', 'eventi culturali', 'sport', 'top eventi sport']
}


def get_category(cat):
	for k, v in cat_dict.items():
		if k != general and cat.lower() in v:
			return k
	return general


def rm_main():
	url = 'https://raw.githubusercontent.com/andreamatt/KDI/master/dataset/trentoTodayE.json'
	obj = json.loads(requests.get(url).text)
	events = [e for e in obj['events'] if 'Title' in e]
	for event in events:
		fill_event(event)
		event['category'] = get_category(event['category'])

	return json.dumps(events)
