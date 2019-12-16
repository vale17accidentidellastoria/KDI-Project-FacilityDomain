import json
import requests
from flashtext import KeywordProcessor
from enum import Enum

months = {
    'gennaio': '01',
    'gen': '01',
    'febbraio': '02',
    'feb': '02',
    'marzo': '03',
    'mar': '03',
    'aprile': '04',
    'apr': '04',
    'maggio': '05',
    'mag': '05',
    'giugno': '06',
    'giu': '06',
    'luglio': '07',
    'lug': '07',
    'agosto': '08',
    'ago': '08',
    'settembre': '09',
    'set': '09',
    'ottobre': '10',
    'ott': '10',
    'novembre': '11',
    'nov': '11',
    'dicembre': '12',
    'dic': '12',
}

days = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']
timeStart = ['from', 'dalle', 'da', 'ore', 'ora', 'alle', 'dal']
timeFinish = ['to', 'a', 'alle']


def rm_main(JSONString):
	with open('C:/Users/andre/Desktop/kdi/scraping/KDI/DBG/format.json', 'w') as outfile:
		json.dump(json.loads(JSONString), outfile, indent="\t")

	obj = json.loads(JSONString)

	def findDay(string, length, index, substring):
		if index >= len(string):
			if length > 0 and length < 3:

				return {'day': substring, 'index': 100}
			else:
				return {'day': '--', 'index': 100}
		if string[index].isdigit():
			length = length + 1
			substring = substring + string[index]
			return findDay(string, length, index + 1, substring)

		elif length > 0 and length < 3:
			return {'day': substring, 'index': index}
		else:
			return findDay(string, 0, index + 1, '')

	def findMonth(string, index, substring):
		if index >= len(string):
			if substring in months:
				return {'month': months[substring], 'index': index}
			else:
				return {'month': '--', 'index': 100}
		if string[index].isalpha():
			substring = substring + string[index]
			return findMonth(string, index + 1, substring)
		else:
			if substring in months:
				return {'month': months[substring], 'index': index}
			else:
				return findMonth(string, index + 1, '')

	def findYear(string, length, index, substring):
		if index >= len(string):
			if length == 4:
				return {'year': substring, 'index': index}
			else:
				return {'year': '--', 'index': 100}

		if string[index].isdigit():
			length = length + 1
			substring = substring + string[index]
			return findYear(string, length, index + 1, substring)

		elif length == 4:
			return {'year': substring, 'index': index}
		else:
			return findYear(string, 0, index + 1, '')

	def findIndex(string, start, array):
		index = start
		find = False
		for element in array:
			new_index = string.find(element, start)
			if new_index <= index and new_index != -1:
				find = True
				index = new_index
		return {'index': index, 'find': find}

	def findHour(string, length, index, substring):
		if index >= len(string):
			if length == 2 or length == 5:
				return {'hour': substring, 'index': 100}
			else:
				return {'hour': '', 'index': 100}
		if string[index].isdigit() or (string[index] == '.' and (length == 2 or length == 5)):
			length = length + 1
			substring = substring + string[index]
			return findHour(string, length, index + 1, substring)
		elif string[index] == '-' and (length == 2 or length == 5):
			return {'hour': substring, 'index': index, 'interval': True}
		elif string[index] == ' ' and string[index] == '-' and (length == 2 or length == 5):
			return {'hour': substring, 'index': index, 'interval': True}
		elif length == 2 or length == 5:
			return {'hour': substring, 'index': index}
		else:
			return findHour(string, 0, index + 1, '')

	def findDayWeek(string, start, array):
		index = -1
		find = False
		giorno = -1
		for i in range(len(array)):
			new_index = string.find(array[i], start)
			if not find and new_index != -1:
				find = True
				index = new_index
				giorno = i
		return {'index': index, 'find': find, 'day': giorno}

	def findDayString(string, index, array):
		start = findIndex(string, 0, timeStart)
		if start['find']:
			first = findDayWeek(string, start['index'], days)
			last = findDayWeek(string, first['index'] + 1, days)

			for i in range(len(days)):
				if i >= first['day'] and i <= last['day']:
					array.append(days[i])
			return array

		day = findDayWeek(string, index, days)
		if day['index'] != -1:
			array.append(days[day['day']])
			return findDayString(string, day['index'] + 1, array)
		else:
			return array

	def uniformData(date):
		if date != '':
			if not '.' in date:
				date += '.00'

		return date

	def findHourString(string, index, array):
		start = findIndex(string, 0, timeStart)
		if start['find']:
			first = findHour(string, 0, 0, '')
			last = findHour(string, 0, first['index'], '')
			first = uniformData(first['hour'])
			last = uniformData(last['hour'])
			rangeDate = first + '-' + last
			array.append(rangeDate)
			return array

		if index <= len(string):
			hour = findHour(string, 0, index, '')
			hourString = uniformData(hour['hour'])
			array.append(hourString)
			return findHourString(string, hour['index'], array)
		else:
			return array

	def findDates(dateArray, string, dayIndex, monthIndex, yearIndex):

		mutex = False
		start = findIndex(string, dayIndex, timeStart)
		day = findDay(string, 0, dayIndex, '')

		if start['find'] and start['index'] < day['index']:
			mutex = True

		if day['index'] == 100:
			month = findMonth(string, monthIndex, '')
		else:
			month = findMonth(string, day['index'], '')

		if month['index'] == 100:
			year = findYear(string, 0, yearIndex, '')
		else:
			year = findYear(string, 0, month['index'], '')

		if day['index'] and month['index'] == 100 and year['index'] == 100:
			print('ok')
		else:
			date = day['day'] + '/' + month['month'] + '/' + year['year']
			dateArray.append(date)
			if mutex:
				dateArray.append(' - ')

			findDates(dateArray, string, day['index'], month['index'], year['index'])

	def arrayCleaning(array):
		outputArray = []
		for i in range(len(array)):
			if array[i] == ' - ':
				outputString = array[i - 1] + '-' + array[i + 1]
				outputArray.append(outputString)
		if outputArray != []:
			return outputArray
		else:
			return array

	array = []
	date = ''
	for event in obj['events']:
		dayArray = []
		findDates(dayArray, event['when'].lower(), 0, 0, 0)
		outputArray = arrayCleaning(dayArray)
		if outputArray == []:
			day = findDayString(event['when'].lower(), 0, [])
			if day != []:
				event['when'] = []
				event['days'] = day
			else:
				event['when'] = []
				event['days'] = []
		else:
			event['when'] = outputArray
			event['days'] = []

		hourArray = []
		findHourString(event['time'].lower(), 0, hourArray)
		if hourArray[0] != '' and hourArray[0] != '-':
			event['time'] = list(set(hourArray))
		else:
			event['time'] = []

		new_dict = {'contact': obj['contact']}
		event.update(new_dict)

	return json.dumps(obj)
