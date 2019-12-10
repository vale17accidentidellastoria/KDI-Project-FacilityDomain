import json
import pandas as pd
import requests

utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)


def rm_main(JSONString):
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/structure.json', 'w') as outfile:
		json.dump(json.loads(JSONString), outfile, indent="\t")

	events = []
	movies = []
	cineworldTrento = json.loads(JSONString)
	for movie in cineworldTrento['movies']:
		movie['director'] = movie['director'][0] if len(movie['director']) > 0 else ''
		movie['genre'] = movie['genre'][0] if len(movie['genre']) > 0 else ''

		scr = ScreeningEvent('')
		m = Movie(movie['originalName'], movie['genre'], movie['length'])
		work_URI = text_to_URI([movie['wikiUrl']])
		work = CreativeWork(movie['title'], movie['director'], movie['year'], movie['wikiUrl'], work_URI)

		for schedule in movie['schedule']:
			gen = GeneralEvent(movie['title'], schedule['Price'], movie['description'], movie['Link'], movie['length'], movie['language'], True,
			                   schedule['location'])
			gen['workURI'] = work_URI

			for t in schedule['time']:
				hours = t['hour'].split('-')
				date = DateTime(schedule['day'], schedule['day'], hours[0], hours[1])
				event = {}
				for k, v in gen.items():
					event[f'GEN_{k}'] = v
				for k, v in scr.items():
					event[f'SCREEN_{k}'] = v
				for k, v in date.items():
					event[f'DATETIME_{k}'] = v
				events.append(event)

				creative_movie = {}
				for k, v in m.items():
					creative_movie[f'MOVIE_{k}'] = v
				for k, v in work.items():
					creative_movie[f'WORK_{k}'] = v
				movies.append(creative_movie)

	return json.dumps({screen: events, creative_movies: movies})
