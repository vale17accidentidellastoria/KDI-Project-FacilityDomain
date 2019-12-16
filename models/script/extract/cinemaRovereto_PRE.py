import json

import requests

fields = ['title', 'Link', 'description', 'genre', 'length', 'time']


def fill_event(e):
	for f in fields:
		e[f] = e.get(f, '')
		if isinstance(e[f], str):
			e[f] = e[f].replace('\n', '; ')


def rm_main():
	url = 'https://raw.githubusercontent.com/andreamatt/KDI/master/dataset/cinemaRovereto.json'
	obj = json.loads(requests.get(url).text)
	info = {
	    'location': "Piazza Rosmini 18/A. Rovereto (TN)",
	    'contact': "0464 421216",
	    'price': "8,50 €",
	    'cinemaURL': "http://www.supercinemarovereto.it/"
	}

	movies = []
	for movie in obj['movies']:
		fill_event(movie)
		if movie['title'] != 'CHIUSO' and movie['time'] != '' and all(not isinstance(dt, str) for dt in movie['time']):
			movies.append(movie)
		movie.update(info)
	obj['movies'] = movies

	return json.dumps(obj)
