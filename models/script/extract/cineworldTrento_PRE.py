import json
import requests


def rm_main():
	url = 'https://raw.githubusercontent.com/vale17accidentidellastoria/KDI-Project-FacilityDomain/master/data/cineworldTrento.json'
	obj = json.loads(requests.get(url).text)
	prices = "https://www.cineworldtrento.it/info-contatti-cinema-trento/"
	standardPrice = "8.50"
	addressModena = "Multiplex G. Modena, Trento"
	addressVittoria = "Supercinema Vittoria, Trento"
	addressRoma = "Cinema Teatro Nuovo Roma, Trento"
	Link = "https://cineworld.18tickets.it/"
	Contact = "+39 0461 983237"
	obj['Link'] = Link
	obj['Contact'] = Contact
	moviesArray = obj["movies"]
	for movie in moviesArray:
		scheduleArray = movie["schedule"]
		for item in scheduleArray:
			item.update({'Price': standardPrice})
			if item["location"] == "Trento - Multisala G. Modena":
				item.update({'location': item["location"] + addressModena})
			elif item["location"] == "Trento - Cinema Teatro Nuovo Roma":
				item.update({'location': item["location"] + addressRoma})
			elif item["location"] == "Trento - Supercinema Vittoria":
				item.update({'location': item["location"] + addressVittoria})
	return json.dumps(obj)
