from flask import Flask, jsonify, request
from hal import HardwareAbstractionLayer

SUCCESS = "OK"
FAILURE = "COULD NOT SET ANGLE"

hal = HardwareAbstractionLayer()

app = Flask(__name__)


@app.route('/move/up', methods=['POST'])
def move_up():
    global hal
    if hal.move_up():
        return SUCCESS
    else:
        return FAILURE


@app.route('/move/down', methods=['POST'])
def move_down():
    global hal
    if hal.move_down():
        return SUCCESS
    else:
        return FAILURE


@app.route('/move/translate', methods=['POST'])
def translate():
    global hal
    delta_x = request.form.get('x')
    delta_y = request.form.get('y')
    if hal.translate(delta_x, delta_y):
        return SUCCESS
    else:
        return FAILURE


if __name__ == "__main__":
    app.run()