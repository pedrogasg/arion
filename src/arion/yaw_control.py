import rospy
from std_msgs.msg import Float32

class YawControl:
    
    def start_stearing(self):
        self.stearing_sub = rospy.Subscriber("/prediction/stearing", Float32, self.updateStearing, queue_size=1)
        self.stearing = 0.0
    
    def updateStearing(self, msg):
        if self.stearing != msg.data:
            self.stearing = msg.data