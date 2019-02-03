import requests
import time

class Communicator:

    BASE_URL = 'http://192.168.43.233:5000'
    TRANSLATE = BASE_URL + '/move/translate'
    UP = BASE_URL + '/move/up'
    DOWN = BASE_URL + '/move/down'

    TIMEOUT = 0.2
    MIN_TIME = 0.02

    def __init__(self):
        self.last_send_time = time.time()

    def send_delta(self, x, y):
        data = {'x': x, 'y': y}
        self._make_request(self.TRANSLATE, data)

    def send_up(self):
        self._make_request(self.UP)

    def send_down(self):
        self._make_request(self.DOWN)

    def _make_request(self, url, data={}):
        cur_time = time.time()
        if cur_time - self.last_send_time >= self.MIN_TIME:
            try:
                requests.post(url, data=data, timeout=self.TIMEOUT)
                self.last_send_time = cur_time
            except:
                pass
        else:
            print("did not send")

