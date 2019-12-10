import json
import re
import requests


def rm_main(JSONString):
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/format.json', 'w') as outfile:
		json.dump(json.loads(JSONString), outfile, indent="\t")

	obj = json.loads(JSONString)
	movies = []
	for movie in obj['movies']:
		times = []
		for dateAndTime in movie['time']:
			hours = dateAndTime['hour']
			hours = hours.split('-')
			for hour in hours:
				hour = hour.replace(' ', '')
				hour = hour.replace('.', ':')
				day = dateAndTime['day']
				day = re.findall(r'\d+\/\d+\/\d+', day)
				day = day[0]
				times.append({"day": day, "hour": hour})
		movie['time'] = times
		movies.append(movie)
	obj['movies'] = movies
	return json.dumps(obj)
