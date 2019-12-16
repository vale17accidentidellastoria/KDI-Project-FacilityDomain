import json
import re

import pandas as pd
import requests

utils_txt = requests.get('https://raw.githubusercontent.com/vale17accidentidellastoria/KDI-Project-FacilityDomain/master/models/script/utils.py').text
exec(utils_txt)


def rm_main(JSONString):
	dictionary = {
	    "Cultural exhibitions and events,": general,
	    "Cultural exhibitions and events,Guided tour,": general,
	    "Dance,Opera and modern ballet,": theatre,
	    "Drama,": theatre,
	    "Meetings and conferences,": talk,
	    "Meetings and conferences,Workshop,": science,
	    "Music,": music,
	    "Music,Classical music concert,": music,
	    "Music,Jazz concert,": music,
	    "exhibition,": general,
	    "exhibition,Art exhibition,": visual,
	    "exhibition,Photographic exhibition,": visual,
	}
	cultura = json.loads(JSONString)
	events = {}
	for day in cultura['result']['events']:
		for eventType in day['tipo_evento']:
			for e in eventType['events']:
				subSubCategory = ""
				for subType in e['tipo_evento']:
					if subType['name'] is not None:
						subSubCategory += subType['name'] + ","
				if len(e['luogo_della_cultura']) == 0:
					e['luogo_della_cultura'].append({"name": ""})
				subSubCategory = dictionary[subSubCategory]
				location = e['comune'][0]['name'] + ", " + e['luogo_svolgimento'] + ", " + e['luogo_della_cultura'][0]['name']
				starts = day['day']['identifier'].split('-')
				startDate = f'{starts[0]}-{starts[1].zfill(2)}-{starts[2].zfill(2)}'
				ends = day['day']['identifier'].split('-')
				endDate = f'{ends[0]}-{ends[1].zfill(2)}-{ends[2].zfill(2)}'
				startTime = ""
				endTime = ""
				time = e['orario_svolgimento']
				tmp = re.findall(r'at \d+\.\d+', time)
				if len(tmp) > 0:
					startTime = tmp[0][3:].replace('.', ':')
				else:
					tmp = re.findall(r'\d+\.\d+', time)
					if len(tmp) == 0:
						tmp = re.findall(r'\d+\,\d+', time)
						if len(tmp) == 0:
							pass
						elif len(tmp) == 1:
							startTime = tmp[0].replace(',', ':')
						elif len(tmp) > 1:
							startTime = tmp[0].replace(',', ':')
							endTime = tmp[1].replace(',', ':')
						pass
					elif len(tmp) == 1:
						startTime = tmp[0].replace('.', ':')
						pass
					elif len(tmp) > 1:
						startTime = tmp[0].replace('.', ':')
						endTime = tmp[1].replace('.', ':')

				if len(startTime) == 4:
					startTime = '0' + startTime + ':00'
				elif len(startTime) == 5:
					startTime = startTime + ':00'

				if len(endTime) == 4:
					endTime = '0' + endTime + ':00'
				elif len(endTime) == 5:
					endTime = endTime + ':00'

				gen = GeneralEvent(e['name'].replace('\n', '. '), e['costi'].replace('\n', '. '), e['description'].replace('\n', '. '),
				                   e['href'].replace('\n', '. '), '', '', '', location.replace('\n', '. '))
				time = DateTime(startDate, endDate, startTime, endTime)

				event = {}
				for k, v in gen.items():
					event[f'GEN_{k}'] = v
				for k, v in time.items():
					event[f'DATETIME_{k}'] = v
				if subSubCategory not in events:
					events[subSubCategory] = []
				events[subSubCategory].append(event)
	return json.dumps(events)
