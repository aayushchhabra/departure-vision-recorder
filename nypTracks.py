from datetime import datetime
from datetime import timedelta
from http.client import RemoteDisconnected

import lib.details_page_page_utils as details_page
import lib.details_page_parse_utils as details_parse
import lib.page_utils as page
import lib.parse_utils as parse
from lib.shuttle_utils import get_shuttle_before


def get_time_to_leave(trains):
    for train in trains:
        now = datetime.now()
        departs_at_arr = train.departs_at.split(':')
        add_number = 12
        if int(departs_at_arr[0]) == 12:
            add_number = 0
        train_time = now.replace(hour=add_number + int(departs_at_arr[0]), minute=int(departs_at_arr[1]))

        shuttle_departs_before = train_time - timedelta(minutes=9) + timedelta(minutes=5)
        if shuttle_departs_before < now:
            continue
        shuttle_time = get_shuttle_before(shuttle_departs_before)
        if shuttle_time == None:
            continue
        leave_at = shuttle_time - timedelta(minutes=5)
        if leave_at < now:
            continue
        return (leave_at, shuttle_time, train_time)

def get_departures(destination = 'Trenton', max_stops = 9):
    html, timestamp = page.get_dv_page(skip_cache=True)
    trains_to = parse.list_departures(html, timestamp)
    return filter_express (trains_to, destination, max_stops)

def filter_express (trains_to, destination = 'Trenton', max_stops = 9):
    result = []
    departures_to_destination = filter(lambda train_to: train_to.dest == destination, trains_to)
    for departure in departures_to_destination:
        html = details_page.fetch_dv_page(departure.train_id)
        stations = details_parse.get_stations(html)
        if len(stations) < max_stops:
            result.append(departure)
    return result

def main(event, context):
    retry_count = 0
    try:
        departures = get_departures('Trenton\xa0✈', 20)
        (leave_at, shuttle_time, train_time) = get_time_to_leave(departures)
        result = "leave at {} \ntake shuttle at {} \ntake train at {}"
        print(result.format(leave_at, shuttle_time, train_time))
        return type(leave_at.strftime("%Y-%m-%d %H:%M"))
    except RemoteDisconnected:
        if ++retry_count < 3:
            print("Remote disconnected, trying again.")
            main(event, context)
        else:
            print("Max retry count reached....Exiting")
            exit(-1)


if __name__ == '__main__':
    print(type(datetime.now().strftime("%Y-%m-%d %H:%M")))
