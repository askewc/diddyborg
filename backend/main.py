from flask import Flask, jsonify

import distance
import motion

app = Flask(__name__, static_url_path='', static_folder='../frontend')

sensors = distance.Sensors()
motors = motion.Motors()


@app.route('/')
def get_status():
    return app.send_static_file('index.html')


@app.route('/api')
def get_status():
    return jsonify({'status': motors.get_status()})


@app.route('/api/distances', methods=['GET'])
def get_distances():
    distances = sensors.read()
    return jsonify({'distances': distances})


@app.route('/api/go/forward/<float:speed>', methods=['GET'])
def go_forward(speed):
    motors.go(speed)
    return get_status()


@app.route('/api/go/backward/<float:speed>', methods=['GET'])
def go_backward(speed):
    motors.go(-speed)
    return get_status()


@app.route('/api/turn/left/<float:speed>', methods=['GET'])
def turn_left(speed):
    motors.turn(speed)
    return get_status()


@app.route('/api/turn/right/<float:speed>', methods=['GET'])
def turn_right(speed):
    motors.turn(-speed)
    return get_status()


@app.route('/api/stop', methods=['GET'])
def stop():
    motors.stop()
    return get_status()


@app.errorhandler(500)
def handle_error(error):
    motors.stop()
    return jsonify({'error': error}), 500


if __name__ == '__main__':
    app.run(host='192.168.85.74', port=8080, debug=True)
