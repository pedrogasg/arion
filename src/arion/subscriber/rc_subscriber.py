import rospy
import numpy as np

from arion.tools import _PWM_ZERO_, _ACTUATORS_

from mavros_msgs.msg import RCIn

class RCSubscriber:
    def start_rc(self):
        self.channels = np.ones(_ACTUATORS_) * _PWM_ZERO_
        self.rc_subscriber = rospy.Subscriber("mavros/rc/in", RCIn, self.update_rc, queue_size=1)

    def update_rc(self, rc):
        self.channels = np.array(rc.channels)