import json
import re
import requests


def rm_main(JSONString):
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/format.json', 'w') as outfile:
		json.dump(json.loads(JSONString), outfile, indent="\t")

	obj = json.loads(JSONString)

	known_times = {'tutto il giorno': '00:00>23:59'}

	events = []
	for event in obj:
		dates = re.findall(r'\d\d/\d\d/\d\d\d\d', event['date'])
		if len(set(dates)) == 1:
			event['startDate'] = event['endDate'] = dates[0].replace('/', '-')
		elif len(set(dates)) == 2:
			event['startDate'] = dates[0].replace('/', '-')
			event['endDate'] = dates[1].replace('/', '-')

		if event['time'] in known_times:
			event['time'] = known_times[event['time']]

		r = r'(?:(?:\d\d|\d)[:.]\d\d)|(?:\d\d|\d)'
		times = re.findall(r, event['time'])
		if len(times) == 1:
			t1 = times[0].replace('.', ':')
			if len(t1) > 2:
				event['startTime'] = t1 + ':00'
			else:
				event['startTime'] = t1 + ':00:00'
		elif len(times) == 2:
			t1 = times[0].replace('.', ':')
			if len(t1) > 2:
				event['startTime'] = t1 + ':00'
			else:
				event['startTime'] = t1 + ':00:00'

			t2 = times[1].replace('.', ':')
			if len(t2) > 2:
				event['endTime'] = t2 + ':00'
			else:
				event['endTime'] = t2 + ':00:00'

		if len(event['startTime']) == 7:
			event['startTime'] = '0' + event['startTime']
		if len(event['endTime']) == 7:
			event['endTime'] = '0' + event['endTime']

		events.append(event)
	return json.dumps(events)
