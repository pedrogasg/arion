import math
import rospy

from geometry_msgs.msg import Pose2D

from arion.subscriber.position_subscriber import CurrentPositionSubscriber

class State2DSubscriber(CurrentPositionSubscriber):
    def start_2d_state(self, cb):
        self.state = Pose2D()
        self.start_current_position()
        self.cb = cb

    def update_current_position(self, pose):
        super().update_current_position(pose)
        p = pose.pose.position
        q = pose.pose.orientation
        self.state.x = p.x
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z); 
        yaw = math.atan2(siny_cosp, cosy_cosp)
        self.state.y = p.y
        self.state.theta = yaw
        self.cb()