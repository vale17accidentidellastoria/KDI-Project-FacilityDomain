import json
import re
import requests


def rm_main(JSONString):
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/format.json', 'w') as outfile:
		json.dump(json.loads(JSONString), outfile, indent="\t")

	obj = json.loads(JSONString)

	known_times = {'tutto il giorno': '00:00-23:59', 'tutta la giornata': '00:00-23:59'}

	events = []
	for event in obj:
		dates = re.findall(r'\d\d/\d\d/\d\d\d\d', event['date'])
		if len(set(dates)) == 1:
			event['startDate'] = event['endDate'] = '-'.join(d.zfill(2) for d in dates[0].split('/')[::-1])
		elif len(set(dates)) == 2:
			event['startDate'] = '-'.join(d.zfill(2) for d in dates[0].split('/')[::-1])
			event['endDate'] = '-'.join(d.zfill(2) for d in dates[1].split('/')[::-1])

		if event['time'] in known_times:
			event['time'] = known_times[event['time']]

		r = r'(?:(?:\d\d|\d)[:.]\d\d)|(?:\d\d|\d)'
		times = re.findall(r, event['time'])
		if len(times) == 1:
			event['startTime'] = times[0].replace('.', ':') + ':00'
		elif len(times) == 2:
			event['startTime'] = times[0].replace('.', ':') + ':00'
			event['endTime'] = times[1].replace('.', ':') + ':00'

		if len(event['startTime']) == 7:
			event['startTime'] = '0' + event['startTime']
		if len(event['endTime']) == 7:
			event['endTime'] = '0' + event['endTime']

		events.append(event)

	return json.dumps(events)
