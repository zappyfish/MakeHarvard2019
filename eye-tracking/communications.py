import requests


class Communicator:

    BASE_URL = 'http://192.168.43.233:5000'
    TRANSLATE = BASE_URL + '/move/translate'
    UP = BASE_URL + '/move/up'
    DOWN = BASE_URL + '/move/down'

    def __init__(self):
        pass

    def send_delta(self, x, y):
        data = {'x': x, 'y': y}
        requests.post(self.TRANSLATE, data=data)

    def send_up(self):
        requests.post(self.UP)

    def send_down(self):
        requests.post(self.DOWN)

