
import rospy
from mavros_msgs.msg import RCIn

class SpeedControl:
    def start_throttle(self):
        self.throttle = 0.0
        self.rc_in = rospy.Subscriber("mavros/rc/in", RCIn, self.update_speed, queue_size=1)

    def update_speed(self, rc):
        throttle = rc.channels[8]
        if throttle > 1000:
            throttle = (throttle / 2000.0) - 0.5
        else:
            throttle = 0
        
        if throttle != self.throttle:
            self.throttle = throttle