import json
import requests
from pandas import DataFrame as DF

utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)


def rm_main(*JSONStrings):
	results = {general: [], science: [], visual: [], music: [], screen: [], theatre: [], talk: [], creative_movies: []}
	for jsonstring in JSONStrings:
		source_events = json.loads(jsonstring)
		for entity_type, event_list in source_events.items():
			results[entity_type].extend(event_list)

	return json.dumps(results)