import datetime
import json
import re


def rm_main(JSONString):
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/format.json', 'w') as outfile:
		json.dump(json.loads(JSONString), outfile, indent="\t")

	obj = json.loads(JSONString)
	movies = []
	for movie in obj['movies']:
		schedules = []
		for schedule in movie['schedule']:
			times = []
			for time in schedule['time']:
				hour = re.findall(r'\d+:\d+', time['hour'])
				hour = hour[0] + ':00'
				time['hour'] = hour
				duration = re.findall(r'\d+', movie['length'])[0]
				end = datetime.timedelta(hours=int(hour[0:2]), minutes=int(hour[3:5])) + datetime.timedelta(minutes=int(duration))
				if end.days > 0:
					end = end + datetime.timedelta(days=-1)
				end = str(end)
				if end[0] == '0':
					end = '0' + end
				end = end[0:5]
				end += ':00'
				time['hour'] += "-" + end
				times.append(time)
			date = schedule['day']
			date = re.findall(r'\d+', date)
			date = date[0]
			if int(date) < 5:
				date = date + "-12-19"
			else:
				date = date + "-11-19"

			date = date[:6] + '20' + date[6:]
			schedule['day'] = date
			schedule['time'] = times
			schedules.append(schedule)
		movie['schedule'] = schedules
		movies.append(movie)
	obj['movies'] = movies
	return json.dumps(obj)
