import requests


class Communicator:

    BASE_URL = 'http://192.168.43.233:5000'
    TRANSLATE = BASE_URL + '/move/translate'
    UP = BASE_URL + '/move/up'
    DOWN = BASE_URL + '/move/down'

    TIMEOUT = 0.1

    def __init__(self):
        pass

    def send_delta(self, x, y):
        data = {'x': x, 'y': y}
        self._make_request(self.TRANSLATE, data)

    def send_up(self):
        self._make_request(self.UP)

    def send_down(self):
        self._make_request(self.DOWN)

    def _make_request(self, url, data={}):
        try:
            requests.post(url, data=data, timeout=self.TIMEOUT)
        except:
            pass

