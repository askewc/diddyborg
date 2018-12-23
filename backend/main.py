from flask import Flask, jsonify, request

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
    _, image = web_cam.image
    return image.tostring()


@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({'status': motors.get_status()})


@app.route('/api/distances', methods=['GET'])
def get_distances():
    distances = sensors.read()
    return jsonify({'distances': distances})


@app.route('/api/move', methods=['POST'])
def move():
    axes = request.get_json()
    motors.set_speed(motion.LEFT, axes[motion.LEFT])
    motors.set_speed(motion.RIGHT, axes[motion.RIGHT])
    return jsonify({'axes': axes})


@app.route('/api/stop', methods=['GET'])
def stop():
    motors.stop()
    return get_status()


@app.errorhandler(500)
def handle_error(error):
    motors.stop()
    return jsonify({'error': error}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
