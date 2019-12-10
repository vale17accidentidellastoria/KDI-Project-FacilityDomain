import json
import requests
from pandas import DataFrame

utils_txt = requests.get('https://raw.githubusercontent.com/andreamatt/KDI/all_fields/scripts/utils.py').text
exec(utils_txt)


def rm_main(JSONstring):
	events = json.loads(JSONstring)

	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/output/UNIFIED.json', 'w') as outfile:
		json.dump(events, outfile, indent='\t')

	event_types = [general, science, visual, music, screen, theatre, talk]
	for t in event_types:
		if len(events[t]) > 0:
			events[t] = DataFrame(events[t], columns=specific_event_columns(t))
		else:
			events[t] = DataFrame(columns=specific_event_columns(t))

	events['facilities'] = DataFrame(events['facilities'])
	events[creative_movies] = DataFrame(events[creative_movies])

	#  events[science]
	#   events[visual], events[music], events[screen], events[theatre], events[talk], events['facilities'], events[creative_movies]

	# for k, v in events.items():
	# 	# save single file
	# 	with open(f'C:/Users/andre/Desktop/kdi/scraping/KDI/output/{k}.json', 'w') as outfile:
	# 		json.dump(v, outfile, indent='\t')

	# 	# convert to DF for output
	# 	if len(events[general]) > 0:
	# 		events[k] = DataFrame(v)
	# 	else:

	return events[general], events[science], events[visual], events[music], events[screen], events[theatre], events[talk], events['facilities'], events[
	    creative_movies]
