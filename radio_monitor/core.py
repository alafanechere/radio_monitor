import requests


# This is an abstract class.
# Followings method must be implemented in child classes :
# * parse_request which returns a dict of metadata
class Collector():
    def __init__(self, radio_name, api_endpoint, crawl_frequency=1):
        self.radio_name = radio_name
        self.api_endpoint = api_endpoint
        self.crawl_frequency = crawl_frequency

    def make_request(self):
        try:
            response = requests.get(self.api_endpoint)
            return response.json()
        except requests.HTTPError, e:
            raise e

    def parse_request(self, json_dump):
        raise NotImplementedError

    def get_current_metadata(self):
        json_response = self.make_request()
        return self.parse_request(json_response)
