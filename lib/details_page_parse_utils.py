from datetime import datetime

from bs4 import BeautifulSoup


class Stations:
    def __init__(self, station):
        self.station = station

    def __str__(self):
        return self.__dict__.__str__()

def get_stations(html):
    """The web scraping function.  When things go wrong, look here.

    Args:
        html (str): html string to parse

    Returns:
        array of Stations that the train will stop at

    """
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')

    stations = []
    for tr in trs:
        a = tr.text.strip()
        dep = Stations(a)
        stations.append(dep)
    return stations
