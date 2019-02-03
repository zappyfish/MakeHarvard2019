import requests


class Communicator:

    BASE_URL = 'http://192.168.43.233:5000'
    TRANSLATE = BASE_URL + '/move/translate'
    UP = BASE_URL + '/move/up'
    DOWN = BASE_URL + '/move/down'

    TIMEOUT = 0.5

    def __init__(self):
        pass

    def send_delta(self, x, y):
        data = {'x': x, 'y': y}
        #requests.post(self.TRANSLATE, data=data, timeout=self.TIMEOUT)

    def send_up(self):
        requests.post(self.UP, timeout=self.TIMEOUT)

    def send_down(self):
        requests.post(self.DOWN, timeout=self.TIMEOUT)

