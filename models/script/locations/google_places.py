from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests
import json
from pandas import DataFrame

API_KEY = 'AIzaSyB211Jj9rzG_io-a_DBNx_aaALMdOaNiug'

MAX_WORKERS = 100

FIELDS = [
    "name", "geometry", "opening_hours", "formatted_address", "permanently_closed", "type", "vicinity", "formatted_phone_number",
    "international_phone_number", "opening_hours", "website", "price_level", "rating", "user_ratings_total"
]

DETAILS_FIELDS = ','.join(FIELDS)

utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)


def Facility(name, telephone, website, mail, hasParking, animalsAllowed, smokingAllowed, isIndoor):
	return locals()


def Timetables(monday, tuestay, wednesday, thursday, friday, saturday, sunday):
	return locals()


def GeoCoordinates(latitude, longitude, altitude, address, addressLocality, addressRegion, postalCode, locationText):
	return locals()


geocoded = {}
search_results = {}
no_results = {}
details_results = {}
errors = {}


def place_search(name):
	if name in search_results:
		return search_results[name]

	url = f'https://maps.googleapis.com/maps/api/place'
	url += f'/findplacefromtext/json?key={API_KEY}&region=it&inputtype=textquery&input={name}'

	response = requests.get(url)

	if response.ok:
		results = response.json()
		search_results[name] = results
		return results
	else:
		errors[name] = response.text
		return None


def place_details(name):
	if name in details_results:
		return details_results[name]
	elif name in no_results:
		return no_results['name']

	if len(search_results[name]['candidates']) == 0:
		no_results[name] = geocode(name)
		return no_results[name]

	candidate = search_results[name]['candidates'][0]
	place_id = candidate['place_id']
	url = f'https://maps.googleapis.com/maps/api/place'
	url += f'/details/json?key={API_KEY}&region=it&place_id={place_id}&fields={DETAILS_FIELDS}'
	response = requests.get(url)

	if response.ok:
		result = response.json()['result']

		complete_position = geocode(result['formatted_address'])
		result['geocoded'] = complete_position

		details_results[name] = result
		return result
	else:
		errors[name] = response.text
		return None


def geocode(name):
	if name in geocoded:
		return geocoded[name]

	url = f'https://maps.googleapis.com/maps/api/geocode'
	url += f'/json?key={API_KEY}&region=it&address={name}'

	response = requests.get(url)

	if response.ok:
		results = response.json()['results']
		if len(results) > 0:
			geocoded[name] = results[0]
		else:
			geocoded[name] = ""
		return geocoded[name]
	else:
		errors[name] = response.text
		return None


def place_search_ALL(locations):
	with PoolExecutor(max_workers=MAX_WORKERS) as executor:
		for _ in executor.map(place_search, locations):
			pass


def place_details_ALL():
	with PoolExecutor(max_workers=MAX_WORKERS) as executor:
		for _ in executor.map(place_details, search_results.keys()):
			pass


def rm_main(eventsJSON):
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/geocoding.json', 'w') as outfile:
		json.dump(json.loads(eventsJSON), outfile, indent='\t')

	#locations = [loc for loc in list(events.loc[:, "locationName"]) if str(loc) != 'nan']
	events = json.loads(eventsJSON)
	locations = []
	event_types = [general, science, visual, music, screen, theatre, talk]
	for t in event_types:
		for e in events[t]:
			if e['GEN_locationText'] != "":
				locations.append(e['GEN_locationText'])
	# to make locations unique
	locations = list(set(locations))

	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/locationsToSearch.json', 'w') as outfile:
		json.dump(locations, outfile, indent='\t')

	for t in event_types:
		for e in events[t]:
			text = e.pop('GEN_locationText')
			if text != "":
				e['GEN_geoURI'] = text_to_URI([text])
			else:
				e['GEN_geoURI'] = ""

	facilities = []

	place_search_ALL(locations)

	place_details_ALL()

	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/places_errors.json', 'w') as outfile:
		json.dump(errors, outfile, indent="\t")
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/places_details.json', 'w') as outfile:
		json.dump(details_results, outfile, indent="\t")
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/places_no_results.json', 'w') as outfile:
		json.dump(no_results, outfile, indent="\t")

	for searched_name, result in details_results.items():
		fac = {}
		if 'point_of_interest' in result['types']:
			name = result['name']
			telephone = result.get('formatted_phone_number', '')
			website = result.get('website', '')
			mail = "No email from google to avoid spamming"
			# other fields are not available from google
			fac = Facility(name, telephone, website, mail, '', '', '', '')

		lat = result['geometry']['location']['lat']
		lng = result['geometry']['location']['lng']
		altitude = ""
		address = result['formatted_address']
		addressLocality = "WHAT IS IT??"
		addressRegion = "WHAT IS IT???"
		postalCode = ''
		for comp in result['geocoded']['address_components']:
			if 'postal_code' in comp['types']:
				postalCode = comp['long_name']
		coordinates = GeoCoordinates(lat, lng, altitude, address, addressLocality, addressRegion, postalCode, text_to_URI([searched_name]))

		timetable = {}
		if 'opening_hours' in result and 'weekday_text' in result['opening_hours']:
			week = result['opening_hours']['weekday_text']
			timetable['Monday'] = week[0][8:]
			timetable['Tuesday'] = week[1][9:]
			timetable['Wednesday'] = week[2][11:]
			timetable['Thursday'] = week[3][10:]
			timetable['Friday'] = week[4][8:]
			timetable['Saturday'] = week[5][10:]
			timetable['Sunday'] = week[6][8:]

		facility = {}
		for k, v in fac.items():
			facility[f'FAC_{k}'] = v
		for k, v in coordinates.items():
			facility[f'GEO_{k}'] = v
		for k, v in timetable.items():
			facility[f'TIMETABLE_{k}'] = v

		facilities.append(facility)

	# no results in google places, used google geocoding
	for searched_name, result in no_results.items():
		if result != "":
			geom = result['geometry']
			location = geom['location']
			lat = location['lat']
			lng = location['lng']
			altitude = ""
			address = result['formatted_address']
			addressLocality = "WHAT IS IT??"
			addressRegion = "WHAT IS IT???"

			postalCode = ''
			for comp in result['address_components']:
				if 'postal_code' in comp['types']:
					postalCode = comp['long_name']
			coordinates = GeoCoordinates(lat, lng, altitude, address, addressLocality, addressRegion, postalCode, text_to_URI([searched_name]))

			facility = {}
			for k, v in coordinates.items():
				facility[f'GEO_{k}'] = v

			facilities.append(facility)

	events['facilities'] = facilities

	return json.dumps(events)
