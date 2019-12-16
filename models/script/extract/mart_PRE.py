import json
import pandas as pd
import requests
import re

utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)


def rm_main():
	url = 'https://raw.githubusercontent.com/andreamatt/KDI/master/dataset/mart.json'
	mart = json.loads(requests.get(url).text)

	dictionary = {
	    "evento": general,
	    "incontro": general,
	    "workshop": general,
	    "visita guidata": general,
	    "laboratorio": science,
	    "conferenza": talk,
	    "inaugurazione": general,
	    "cinema": screen,
	}

	for event in mart:
		if "locationName" not in event:
			event['locationName'] = ""

		email = re.search(r'[\w\.-]+@[\w\.-]+', event['comment'])
		event['contact'] = email.group(0)

		cost = re.search(r'Costo: € \d+', event['comment'])
		if cost is not None:
			event['cost'] = cost.group(0)
		else:
			event['cost'] = 'free'
		event['link'] = 'mart.trento.it/agenda.jsp'

		if event['location'] == None:
			event['location'] = ""

		if event['category'] in dictionary:
			event['category'] = dictionary[event['category']]
		else:
			event['category'] = general

	return json.dumps(mart)
