from bs4 import BeautifulSoup
import datetime
import requests


# This is an abstract class.
# Followings method must be implemented in child classes :
# * parse_request which returns a dict of metadata
class Collector():
    RADIO_NAME = NotImplemented
    _API_ENDPOINT = NotImplemented

    def __init__(self, crawl_frequency=1):
        self.crawl_frequency = crawl_frequency

    def make_request(self):
        try:
            response = requests.get(self._API_ENDPOINT)

            try:
                return response.json()
            except ValueError:
                return response.text

        except requests.HTTPError, e:
            raise e

    def parse_response(self, json_dump, current_time):
        # should return a dict of metadata
        raise NotImplementedError

    def get_current_metadata(self):
        json_response = self.make_request()
        current_time = datetime.datetime.now()
        return self.parse_response(json_response, current_time)


class Metadata():

    def __init__(self, title, artist, broadcaster, broadcast_time, album=None, year=None, label=None):
        self.title = title
        self.artist = artist
        self.album = album
        self.year = year
        self.label = label
        self.broadcaster = broadcaster
        self.broadcast_time = broadcast_time

    def __str__(self):
        return "Title: {}\n" \
               "Artist: {}\n" \
               "Album: {}\n" \
               "Label: {}\n" \
               "Year: {}\n" \
               "Broadcast_time: {}\n" \
               "Broadcaster: {}".format(self.title.encode('ascii', 'ignore'),
                                        self.artist.encode('ascii', 'ignore'),
                                        self.album,
                                        self.label,
                                        self.year,
                                        self.broadcast_time,
                                        self.broadcaster)


class FipCollector(Collector):
    RADIO_NAME = "FIP"
    _API_ENDPOINT = "http://www.fipradio.fr/livemeta/7"

    def __init__(self, crawl_frequency=1):
        Collector.__init__(self, crawl_frequency)

    def parse_response(self, json_dump, current_time):
        metadata = None

        for _, track in json_dump['steps'].iteritems():
            track['start'] = datetime.datetime.fromtimestamp(track['start'])
            track['end'] = datetime.datetime.fromtimestamp(track['end'])

            if 'title' in track and 'authors' in track and track['start'] < current_time < track['end']:
                title = track['title'].lower()
                artist = track['authors'].lower()
                album = track['titreAlbum'].lower()
                label = track['label'].lower()
                year = track['anneeEditionMusique']
                metadata = Metadata(title, artist, self.RADIO_NAME, current_time, album=album, label=label, year=year)
                break

        return metadata


class NovaCollector(Collector):
    RADIO_NAME = "Nova"
    _API_ENDPOINT = "http://www.novaplanet.com/radionova/ontheair"

    def __init__(self, crawl_frequency=1):
        Collector.__init__(self, crawl_frequency)

    def parse_response(self, json_dump, current_time):
        metadata = None
        track = json_dump['track']
        if len(track['id']) > 0:
            soup = BeautifulSoup(track['markup'])
            artist = soup.find("div", class_="artist").getText().strip().lower()
            title = soup.find("div", class_="title").getText().strip().lower()
            metadata = Metadata(title, artist, self.RADIO_NAME, current_time)

        return metadata


class FunRadioCollector(Collector):
    RADIO_NAME = "FunRadio"
    _API_ENDPOINT = "http://www.funradio.fr/direct/timeline"

    def __init__(self, crawl_frequency=1):
        Collector.__init__(self, crawl_frequency)

    def parse_response(self, html_dump, current_time):
        soup = BeautifulSoup(html_dump)
        title = soup.find("h2", class_="song-title").getText().strip().lower()
        artist = soup.find("p", class_="song-artist").getText().strip().lower()
        metadata = Metadata(title, artist, self.RADIO_NAME, current_time)

        return metadata
