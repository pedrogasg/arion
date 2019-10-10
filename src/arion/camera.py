import cv2
import atexit
import traitlets
import threading
import numpy as np



class GStreamerCamera(traitlets.HasTraits):

    value = traitlets.Any()
    width = traitlets.Integer(default_value=320)
    height = traitlets.Integer(default_value=180)
    running = traitlets.Bool(default_value=False)
    src = traitlets.Integer(default_value=0)
    rate = traitlets.Integer(default_value=30)
    native_width = traitlets.Integer(default_value=1280)
    native_height = traitlets.Integer(default_value=720)

    @staticmethod
    def encode_image(image):
        return bytes(cv2.imencode('.jpg', value)[1])
    
    def __init__(self, *args, **kwargs):
        super(GStreamerCamera, self).__init__(*args, **kwargs)

        self.value = np.empty((self.height, self.width, 3), dtype=np.uint8)
        self._running = False
        try:
            self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)

            re, image = self.cap.read()

            if not re:
                raise RuntimeError('Could not read image from camera.')
        except:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.cap.release)

    def _gst_str(self):
        return 'nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
                self.src, self.native_width, self.native_height, self.rate, self.width, self.height)
    
    def _read(self):
        re, image = self.cap.read()
        if re:
            return image
        else:
            raise RuntimeError('Could not read image from camera')
        
    def read(self):
        if self._running:
            raise RuntimeError('Cannot read directly while camera is running')
        self.value = self._read()
        return self.value
    
    def _capture_frames(self):
        while True:
            if not self._running:
                break
            self.value = self._read()
            
    @traitlets.observe('running')
    def _on_running(self, change):
        if change['new'] and not change['old']:
            # transition from not running -> running
            self._running = True
            self.thread = threading.Thread(target=self._capture_frames)
            self.thread.start()
        elif change['old'] and not change['new']:
            # transition from running -> not running
            self._running = False
            self.thread.join()