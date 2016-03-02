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
        self.title = title.strip().lower()
        self.artist = artist.strip().lower()

        if album is not None:
            self.album = album.strip().lower()
        else:
            self.album = album

        if label is not None:
            self.label = label.strip().lower()
        else:
            self.label = label

        self.year = year
        self.broadcaster = broadcaster
        self.broadcast_time = broadcast_time

    def __str__(self):
        try:
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
        except UnicodeEncodeError:
            return "Title: {}\n" \
                   "Artist: {}\n" \
                   "Album: {}\n" \
                   "Label: {}\n" \
                   "Year: {}\n" \
                   "Broadcast_time: {}\n" \
                   "Broadcaster: {}".format(self.title.encode('ascii', 'ignore'),
                                            self.artist.encode('ascii', 'ignore'),
                                            self.album.encode('ascii', 'ignore'),
                                            self.label.encode('ascii', 'ignore'),
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
                title = track['title']
                artist = track['authors']
                album = track['titreAlbum']
                label = track['label']
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
            artist = soup.find("div", class_="artist").getText()
            title = soup.find("div", class_="title").getText()
            metadata = Metadata(title, artist, self.RADIO_NAME, current_time)

        return metadata


class FunRadioCollector(Collector):
    RADIO_NAME = "FunRadio"
    _API_ENDPOINT = "http://www.funradio.fr/direct/timeline"

    def __init__(self, crawl_frequency=1):
        Collector.__init__(self, crawl_frequency)

    def parse_response(self, html_dump, current_time):
        soup = BeautifulSoup(html_dump)
        title = soup.find("h2", class_="song-title").getText()
        artist = soup.find("p", class_="song-artist").getText()
        metadata = Metadata(title, artist, self.RADIO_NAME, current_time)

        return metadata


class NrjCollector(Collector):
    RADIO_NAME = "NRJ"
    _API_ENDPOINT = "http://players.nrjaudio.fm/wr_api/live/fr?id_wr=158&cp=UTF8&fmt=json&act=get_cur"

    def __init__(self, crawl_frequency=1):
        Collector.__init__(self, crawl_frequency)

    def parse_response(self, json_dump, current_time):
        track = json_dump["itms"][0]
        if len(track['itn']) > 0 :
            return Metadata(track['tit'], track['art'], self.RADIO_NAME, current_time)
        else:
            return None


class SkyrockCollector(Collector):
    RADIO_NAME = "Skyrock"
    _API_ENDPOINT = "http://skyrock.fm/api/v3/player/onair'"

    def __init__(self, crawl_frequency=1):
        Collector.__init__(self, crawl_frequency)

    def parse_response(self, json_dump, current_time):
        track = json_dump["schedule"][-1]
        track['info']['start_ts'] = datetime.datetime.fromtimestamp(float(track['info']['start_ts']))
        track['info']['end_ts'] = datetime.datetime.fromtimestamp(float(track['info']['end_ts']))

        if track['info']['start_ts'] < current_time < track['info']['end_ts']:
            return Metadata(track['info']['title'], track['artists'][0]['name'], self.RADIO_NAME, current_time)
        else:
            return None