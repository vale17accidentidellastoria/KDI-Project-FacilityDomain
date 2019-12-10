from urllib.parse import quote

general = 'Event'
science = 'ScienceEvent'
visual = 'VisualArtsEvent'
music = 'MusicEvent'
screen = 'ScreeningEvent'
theatre = 'TheatreEvent'
talk = 'TalkEvent'
creative_movies = 'Movie'
BASE_URI = "http://www.semanticweb.org/facilitiesEventsOntology"


def GeneralEvent(name, price, description, website, duration, language, isTicketAvailable, locationText):
	return locals()


def ScienceEvent(topic):
	return locals()


def VisualArtsEvent(artMovement):
	return locals()


def MusicEvent(genre, performer):
	return locals()


def ScreeningEvent(salaNumber):
	return locals()


def TheatreEvent(interpreters):
	return locals()


def TalkEvent(hasPresentation, isConference):
	return locals()


def VisualArtwork(style):
	return locals()


def MusicPlaylist(songs):
	return locals()


def Movie(originalName, genre, duration):
	return locals()


def Play(genre):
	return locals()


def Book(pages, genre, editor):
	return locals()


def DateTime(startDate, endDate, startTime, endTime):
	return locals()


def Schedule(byDay, byMonth, byMonthDay, repeatCount, repeatFrequency):
	return locals()


def Discount(young, students, children, groups):
	return locals()


def CreativeWork(name, creator, createDate, url, URI):
	return locals()


def Facility(name, telephone, website, mail, hasParking, animalsAllowed, smokingAllowed, isIndoor):
	return locals()


def Timetables(monday, tuestay, wednesday, thursday, friday, saturday, sunday):
	return locals()


def GeoCoordinates(latitude, longitude, altitude, address, addressLocality, addressRegion, postalCode, URI):
	return locals()


def text_to_URI(labels):
	result = BASE_URI
	for l in labels:
		if l != "" and l != None and isinstance(l, str):
			result += f'/{quote(l)}'
		else:
			result += f'/{quote("unknown")}'
	return result


def specific_event_columns(category):
	general_cols = [f'GEN_{v}' for v in list(GeneralEvent("", "", "", "", "", "", "", "").keys())[:-1]]
	uri_cols = ['GEN_geoURI', 'GEN_workURI']
	datetime_cols = [f'DATETIME_{v}' for v in DateTime("", "", "", "").keys()]
	schedule_cols = [f'SCHEDULE_{v}' for v in Schedule("", "", "", "", "").keys()]

	col_map = {
	    general: general_cols + uri_cols + datetime_cols + schedule_cols,
	    science: general_cols + [f'SCIENCE_{v}' for v in ScienceEvent("").keys()] + uri_cols + datetime_cols + schedule_cols,
	    visual: general_cols + [f'VISUAL_{v}' for v in VisualArtsEvent("").keys()] + uri_cols + datetime_cols + schedule_cols,
	    music: general_cols + [f'MUSIC_{v}' for v in MusicEvent("", "").keys()] + uri_cols + datetime_cols + schedule_cols,
	    screen: general_cols + [f'SCREEN_{v}' for v in ScreeningEvent("").keys()] + uri_cols + datetime_cols + schedule_cols,
	    theatre: general_cols + [f'THEATRE_{v}' for v in TheatreEvent("").keys()] + uri_cols + datetime_cols + schedule_cols,
	    talk: general_cols + [f'TALK_{v}' for v in TalkEvent("", "").keys()] + uri_cols + datetime_cols + schedule_cols
	}

	return col_map[category]
