import rospy
import threading
from copy import deepcopy
from nav_msgs.msg import Odometry

class VisionOdometer:
    def __init__(self, topic):
        self.read_lock = threading.Lock()
        self.odom = Odometry()
        self.odom_sub = rospy.Subscriber(topic, Odometry, self.receive_pose)

    def is_started(self):
        return self.odom is not None

    def receive_pose(self, odom):
        with self.read_lock:
            self.odom = odom

    def read(self):
        with self.read_lock:
            odom = deepcopy(self.odom)
        return odom

    


