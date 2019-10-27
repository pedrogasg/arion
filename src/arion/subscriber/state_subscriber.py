import math
import rospy

from geometry_msgs.msg import Point

from arion.subscriber.position_subscriber import CurrentPositionSubscriber

class State2DSubscriber(CurrentPositionSubscriber):
    def start_2d_state(self):
        self.state = Point()
        self.start_current_position()

    def update_current_position(self, pose):
        super().update_current_position(pose)
        p = pose.pose.position
        q = pose.pose.orientation
        self.state.x = p.x
        self.state.y = p.y
        self.state.z = math.asin(2 * q.x * q.y + 2 * q.z * q.w)