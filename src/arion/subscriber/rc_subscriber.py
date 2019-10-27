import rospy
import numpy as np
from mavros_msgs.msg import RCIn

class RCSubscriber:
    _ACTUATORS_ = 8
    _ZERO_ = 1500
    def start_rc(self):
        self.channels = np.ones(RCSubscriber._ACTUATORS_) * RCSubscriber._ZERO_
        self.rc_subscriber = rospy.Subscriber("mavros/rc/in", RCIn, self.update_rc, queue_size=1)

    def update_rc(self, rc):
        self.channels = rc.channels