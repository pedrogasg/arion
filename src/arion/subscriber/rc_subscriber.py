import rospy
from mavros_msgs.msg import RCIn

class RCSubscriber:
    _ACTUATORS_ = 8
    def start_rc(self):
        self.channels = np.ones(_ACTUATORS_) * 1500
        self.rc_subscriber = rospy.Subscriber("mavros/rc/in", RCIn, self.update_speed, queue_size=1)

    def update_rc(self, rc):
        self.channels = rc.channels