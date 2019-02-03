from flask import Flask, jsonify, request
from hal import HardwareAbstractionLayer

SUCCESS = "OK"
FAILURE = "COULD NOT SET ANGLE"

hal = HardwareAbstractionLayer()

app = Flask(__name__)


@app.route('/move/up', methods=['POST'])
def move_up():
    global hal
    if hal.move_instrument_up():
        return SUCCESS
    else:
        return FAILURE


@app.route('/move/down', methods=['POST'])
def move_down():
    global hal
    if hal.move_instrument_down():
        return SUCCESS
    else:
        return FAILURE


@app.route('/move/translate', methods=['POST'])
def translate():
    global hal
    delta_x = float(request.form.get('y')) # TODO: Change this as you change your whiteboard coordinate system
    delta_y = -1 * float(request.form.get('x'))
    if hal.translate_instrument(delta_x, delta_y):
        return SUCCESS
    else:
        return FAILURE


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)