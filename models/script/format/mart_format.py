import json

import re


def rm_main(JSONString):
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/format.json', 'w') as outfile:
		json.dump(json.loads(JSONString), outfile, indent="\t")

	mart = json.loads(JSONString)
	events = []
	for event in mart:
		times = re.findall(r'\d+:\d+', event['time'])
		time = ""
		if len(times) > 0:
			time = times[0] + ':00'
		if len(times) > 1:
			time += "-" + times[1] + ':00'
		event['time'] = time

		date = re.findall(r'\d+\/\d+', event['date'])[0].replace('/', '-') + '-2019'
		event['date'] = '-'.join(d.zfill(2) for d in date.split('-')[::-1])

		events.append(event)
	mart = events

	return json.dumps(mart)
