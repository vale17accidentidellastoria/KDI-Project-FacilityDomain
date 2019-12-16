import json
import pandas as pd
import requests

utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)


def rm_main(JSONString):

	events = []
	movies = []
	cinemaRovereto = json.loads(JSONString)
	for movie in cinemaRovereto['movies']:
		movie['director'] = movie['director'][0] if len(movie['director']) > 0 else ''
		movie['genre'] = movie['genre'][0] if len(movie['genre']) > 0 else ''

		gen = GeneralEvent(movie['title'], movie['price'], movie['description'], movie['cinemaURL'], movie['length'], movie['language'], True,
		                   movie['location'])
		scr = ScreeningEvent('')
		m = Movie(movie['originalName'], movie['genre'], movie['length'])
		work_URI = text_to_URI([movie['wikiUrl']])
		gen['workURI'] = work_URI
		work = CreativeWork(movie['title'], movie['director'], movie['year'], movie['wikiUrl'], work_URI)

		for dateAndTime in movie['time']:
			for hour in dateAndTime['hour'].split('-'):
				date = DateTime(dateAndTime['day'], dateAndTime['day'], hour, '')
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
