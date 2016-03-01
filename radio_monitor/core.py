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
            return response.json()
        except requests.HTTPError, e:
            raise e

    def parse_request(self, json_dump, current_time):
        # should return a dict of metadata
        raise NotImplementedError

    def get_current_metadata(self):
        json_response = self.make_request()
        current_time = datetime.datetime.now()
        return self.parse_request(json_response, current_time)


class Metadata():

    def __init__(self, title, artist, broadcaster, broadcast_time):
        self.title = title
        self.artist = artist
        self.broadcaster = broadcaster
        self.broadcast_time = broadcast_time


class FipCollector(Collector):
    RADIO_NAME = "FIP"
    _API_ENDPOINT = "http://www.fipradio.fr/livemeta/7"

    def __init__(self, crawl_frequency=1):
        Collector.__init__(self, crawl_frequency)

    def parse_request(self, json_dump, current_time):
        metadata = None

        for key, value in json_dump['steps'].iteritems():
            if value['start'] < current_time < value['stop']:
                title = value['title']
                artist = value['authors']
                metadata = Metadata(title, artist, self.RADIO_NAME, current_time)
                break

        return metadata