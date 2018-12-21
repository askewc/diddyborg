import time

from flask import Flask, jsonify, request

import distance
import motion

app = Flask(__name__)
sensors = distance.Sensors()
motors = motion.Motors()


@app.route('/')
def get_status():
	return jsonify({'status': motors.get_status()})


@app.route('/distances', methods=['GET'])
def get_distances():
	distances = sensors.read()
	return jsonify({'distances': distances})


@app.route('/go/forward/<float:speed>', methods=['GET'])
def go_forward(speed):
	motors.go(speed)
	return get_status()


@app.route('/go/backward/<float:speed>', methods=['GET'])
def go_backward(speed):
	motors.go(-speed)
	return get_status()


@app.route('/turn/left/<float:speed>', methods=['GET'])
def turn_left(speed):
	motors.turn(speed)
	return get_status()


@app.route('/turn/right/<float:speed>', methods=['GET'])
def turn_right(speed):
	motors.turn(-speed)
	return get_status()


@app.route('/stop', methods=['GET'])
def stop():
	motors.stop()
	return get_status()


@app.errorhandler(500)
def handle_error(error):
	motors.stop()
	return jsonify({'error': error}), 500


if __name__ == '__main__':
	app.run(host='192.168.85.74', port=8080, debug=True)