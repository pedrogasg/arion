import rospy
import threading
from copy import deepcopy
from nav_msgs.msg import Odometry

class VisionOdometer:
    def __init__(self):
        self.read_lock = threading.Lock()
        self.odom = None
        self.odom_sub = rospy.Subscriber('/camera/odom/sample', Odometry, self.receive_pose)

    def receive_pose(self, odom):
        with self.read_lock:
            self.odom = odom

    def read(self):
        with self.read_lock:
            odom = deepcopy(odom)
        return odom


        
    


