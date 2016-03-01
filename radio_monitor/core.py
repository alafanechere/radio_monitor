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

    def parse_request(self, json_dump):
        # should return a dict of metadata
        raise NotImplementedError

    def get_current_metadata(self):
        json_response = self.make_request()
        return self.parse_request(json_response)


class Metadata():

    def __init__(self, title, artist, broadcaster, broadcast_time):
        self.title = title
        self.artist = artist
        self.broadcaster = broadcaster
        self.broadcast_time = broadcast_time
