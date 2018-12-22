from flask import Flask, jsonify

import distance
import image_capture
import motion

app = Flask(__name__, static_url_path='', static_folder='../frontend')

sensors = distance.Sensors()
motors = motion.Motors()
web_cam = image_capture.WebCam()


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/cam.jpg', methods=['GET'])
def get_web_cam_image():
    return web_cam.image.tostring()


@app.route('/api', methods=['GET'])
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
    app.run(host='0.0.0.0', port=80, debug=True)
