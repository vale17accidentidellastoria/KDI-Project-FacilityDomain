import json
import requests

utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)

cat_dict = {
    science: ['escursioni', 'religione', 'auto e moto'],
    visual: ['mostre', 'mercatini', 'fiere', 'inaugurazioni', 'turismo', 'moda'],
    music: ['sagre', 'concerti', 'disco&feste'],
    screen: ['cinema'],
    theatre: ['teatri'],
    talk: ['incontri', 'manifestazioni', 'talk'],
    general: ['cibo e vino', 'sport', 'fitness', 'hobby', 'promozioni']
}


def get_category(cat):
	for c in cat.split(', '):
		for k, v in cat_dict.items():
			if k != general and c.lower() in v:
				return k
	return general


fields = ['Title', 'link', 'category', 'location', 'Prices', 'date', 'time', 'description', 'startDate', 'endDate', 'startTime', 'endTime']


def fill_event(e):
	for f in fields:
		e[f] = e.get(f, '').replace('\n', '; ')


def rm_main():
	url = 'https://raw.githubusercontent.com/andreamatt/KDI/master/dataset/visitTrentino.json'
	obj = json.loads(requests.get(url).text)
	events = [e for e in obj['events'] if 'Title' in e]
	for event in events:
		if 'category' in event:
			event['category'] = event['category'][len('Tipologia\n'):]
		if 'location' in event:
			event['location'] = event['location'][len('Località\n'):]
		if 'date' in event:
			event['date'] = event['date'][len('Periodo\n'):]

		fill_event(event)

		event['category'] = get_category(event['category'])

	return json.dumps(events)
