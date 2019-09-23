#!/usr/bin/env python3
import cv2
import threading


class GStreamerCamera:
    _DEFAULT_RATE_ = 120
    _DEFAULT_WIDTH_ = 1280
    _DEFAULT_HEIGHT_ = 720

    def __init__(self, src=0, width=410, height=308, flip_mode=1):
        self.src = src
        self.width = width
        self.height = height
        self.flip_mode = flip_mode
        self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.cap.set(var1, var2)
    
    def _gst_str(self):
        return 'nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=(int)%d ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
                self.src, self._DEFAULT_WIDTH_, self._DEFAULT_HEIGHT_, self._DEFAULT_RATE_, self.flip_mode, self.width, self.height)

    def start(self):
        if self.started:
            rospy.loginfo('[!] Asynchroneous video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.stop()
        self.cap.release()