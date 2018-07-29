from datetime import datetime, timedelta

SHUTTLE_SCHEDULE_FILE = 'shuttle_data/schedule.txt'
departures = []

def get_shuttle_before(time):
    if len(departures) == 0:
        parse_shuttle_schedule()
    now = datetime.now()
    for departure in departures:
        if departure < time and departure > now:
            return departure


def parse_shuttle_schedule():
    with open(SHUTTLE_SCHEDULE_FILE, 'r') as f:
        print("reading %s" % SHUTTLE_SCHEDULE_FILE)
        for line in iter(lambda: f.readline(), ''):
            departure_time_arr = line.split(':')
            now = datetime.now()
            departure_time = now.replace(hour=12 + int(departure_time_arr[0]), minute=int(departure_time_arr[1]))
            departures.append(departure_time)
