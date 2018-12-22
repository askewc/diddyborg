import time
from threading import Event, Lock, Thread

import cv2
import numpy
from picamera import PiCamera
from picamera.array import PiRGBArray

CV2_JPEG_QUALITY_FLAG = [cv2.IMWRITE_JPEG_QUALITY, 80]


class ImageStreamingThread(Thread):
    def __init__(self, camera):
        super(ImageStreamingThread, self).__init__()

        self.stream = PiRGBArray(camera)
        self.event = Event()
        self.is_terminated = False
        self.lock = Lock()
        self.image = None

        self.start()
        self.begin = 0

    def run(self):
        while not self.is_terminated:
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    self.lock.acquire()
                    image = cv2.imencode('.jpg', self.stream.array, CV2_JPEG_QUALITY_FLAG)
                    if image is not None:
                        self.image = image
                    self.lock.release()
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()


class ImageCaptureThread(Thread):
    def __init__(self, camera, image_streaming_thread):
        super(ImageCaptureThread, self).__init__()

        self.camera = camera
        self.image_streaming_thread = image_streaming_thread
        self.is_terminated = False
        self.start()

    def run(self):
        print('running in image_capture thread')
        self.camera.capture_sequence(self.trigger_image_streaming(), format='bgr', use_video_port=True)
        self.image_streaming_thread.is_terminated = True
        self.image_streaming_thread.join()

    def trigger_image_streaming(self):
        while not self.is_terminated:
            if self.image_streaming_thread.event.is_set():
                time.sleep(0.01)
            else:
                yield self.image_streaming_thread.stream
                self.image_streaming_thread.event.set()


class WebCam:
    def __init__(self, resolution=(240, 192), frame_rate=30):
        self.resolution = resolution

        self.pi_camera = PiCamera()
        self.pi_camera.resolution = resolution
        self.pi_camera.framerate = frame_rate

        print('got pi cam')

        # self.streaming_thread = ImageStreamingThread(self.pi_camera)
        time.sleep(2)
        # self.capture_thread = ImageCaptureThread(self.pi_camera, self.streaming_thread)

    @property
    def image(self):
        self.streaming_thread.lock.acquire()
        image = self.streaming_thread.image
        self.streaming_thread.lock.release()

        image = numpy.zeros(self.resolution + (3,), numpy.uint8) if image is None else image

        return image

    def close(self):
        self.capture_thread.join()
        self.capture_thread.is_terminated = True

        self.streaming_thread.join()
        self.streaming_thread.is_terminated = True

        del self.pi_camera
