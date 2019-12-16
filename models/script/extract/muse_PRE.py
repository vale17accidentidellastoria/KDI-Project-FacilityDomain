import json
import requests
from flashtext import KeywordProcessor

utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)


def rm_main():
	ScienceEvent = {"scienza", "universo", "geologia", "biologia", "scientifico", "scientifica", "scienziato", "scienzata"}
	VisualArtEvent = {"pittura", "scultura", "artista", "artisti", "art", "opere", "opera", "part"}
	keyPArt = KeywordProcessor()
	keyPScience = KeywordProcessor()
	for element in ScienceEvent:
		keyPScience.add_keyword(element)
	for element in VisualArtEvent:
		keyPArt.add_keyword(element)

	url = 'https://raw.githubusercontent.com/andreamatt/KDI/master/dataset/muse.json'
	obj = json.loads(requests.get(url).text)
	eventsArray = obj["events"]
	while {} in eventsArray:
		eventsArray.remove({})
	for event in eventsArray:
		for k, v in event.items():
			event[k] = v.replace('\n', '; ')
		artList = keyPArt.extract_keywords(event["description"])
		scienceList = keyPScience.extract_keywords(event["description"])
		if len(artList) > len(scienceList):
			event.update({'Subcategory': visual})
		elif len(artList) <= len(scienceList):
			event.update({'Subcategory': science})

	obj["events"] = eventsArray
	return json.dumps(obj)
