import os
import socket
import urllib.request
from datetime import datetime

from lib.details_page_parse_utils import get_stations

DV_BASE = "http://dv.njtransit.com/mobile/train_stops.aspx?sid={}&train={}"
DEFAULT_DEPARTURE_STATION = "NP"

CACHE_PATH="dv_details_data"

def fetch_dv_page(train, station=DEFAULT_DEPARTURE_STATION):
    url = DV_BASE.format(station, train)
    with urllib.request.urlopen(url, timeout=30) as response:
        html = response.read()
    return html


def cache_dv_page(page, station=DEFAULT_DEPARTURE_STATION, path=CACHE_PATH):
    now = datetime.today()
    if not os.path.isdir(path):
        os.mkdir(path)
    name = "dvd_%s_%s.html" % (station, now.isoformat())
    with open(os.path.join(path, name), 'wb') as f:
        f.write(page)
    return os.path.join(path, name)
