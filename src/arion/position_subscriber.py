import rospy
from geometry_msgs.msg import PoseStamped

class CurrentPositionSubscriber:
    def start_position(self):
        self.current_position = PoseStamped()
        self.current_position_sub = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, self.update_current_position)

    def update_current_position(self, pose):
        self.current_position = pose
