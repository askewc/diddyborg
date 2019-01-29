import time
from flask import Flask, jsonify, request
from threading import Timer

from roboclaw import Roboclaw

E_STOP_DURATION = 10
LEFT = 'left'
RIGHT = 'right'
rc = Roboclaw("/dev/ttyACM0",115200)
rc.Open()
address = 0x80
app = Flask(__name__, static_url_path='', static_folder='../frontend')

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/api/stop', methods=['GET'])
def stop():
    rc.ForwardM1(address, 0)
    rc.ForwardM2(address, 0)
    return True

last_command_time = 0


def e_stop():
    if time.time() - last_command_time > E_STOP_DURATION:
        stop()


timer = Timer(1, e_stop)
timer.start()

@app.route('/api/move', methods=['POST'])
def move():
    last_command_time = time.time()

    axes = request.get_json()

    if axes[LEFT] >= 0:
	rc.ForwardM1(address, int(127 * axes[LEFT]))
    else:
	rc.BackwardM1(address, int(-127 * axes[LEFT]))

    if axes[RIGHT] >= 0:
	rc.ForwardM2(address, int(127 * axes[RIGHT]))
    else:
	rc.BackwardM2(address, int(-127 * axes[RIGHT]))

    return jsonify({'axes': axes})


@app.errorhandler(500)
def handle_error(error):
    stop()
    return jsonify({'error': error}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
