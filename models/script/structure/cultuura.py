import json
import re

import pandas as pd
import requests

utils_txt = requests.get('https://raw.githubusercontent.com/vale17accidentidellastoria/KDI-Project-FacilityDomain/master/models/script/utils.py').text
exec(utils_txt)

def rm_main(JSONString):
	dictionary = {
		"Cultural exhibitions and events,"            : "GeneralEvent",
		"Cultural exhibitions and events,Guided tour,": "GeneralEvent",
		"Dance,Opera and modern ballet,"              : "TheatreEvent",
		"Drama,"                                      : "TheatreEvent",
		"Meetings and conferences,"                   : "TalkEvent",
		"Meetings and conferences,Workshop,"          : "ScienceEvent",
		"Music,"                                      : "MusicEvent",
		"Music,Classical music concert,"              : "MusicEvent",
		"Music,Jazz concert,"                         : "MusicEvent",
		"exhibition,"                                 : "GeneralEvent",
		"exhibition,Art exhibition,"                  : "VisualArtsEvent",
		"exhibition,Photographic exhibition,"         : "VisualArtsEvent",
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
				location = e['comune'][0]['name'] + ", " + e['luogo_svolgimento'] + ", " + e['luogo_della_cultura'][0][
					'name']
				startDate = day['day']['identifier']
				endDate = day['day']['identifier']
				startTime = ""
				endTime = ""
				time = e['orario_svolgimento']
				tmp = re.findall(r'at \d+\.\d+', time)
				if len(tmp):
					startTime = tmp[0]
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
						
				gen = GeneralEvent(e['name'], e['costi'], e['description'], e['href'], '', '', '', location)
				time = Time(startDate, endDate, startTime, endTime)
				
				event = {}
				for k, v in gen.items():
					event[f'GEN_{k}'] = v
				for k, v in time.items():
					event[f'TIME_{k}'] = v
				if subSubCategory not in events:
					events[subSubCategory] = []
				events[subSubCategory].append(event)
	return json.dumps(events)
