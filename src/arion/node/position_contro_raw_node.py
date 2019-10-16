#!/usr/bin/env python3
import rospy
from arion.offboard import OffboardControl
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import PositionTarget

class PositionControlRawNode(OffboardControl):

    def __init__(self):
        self.message_pub = rospy.Publisher('mavros/setpoint_raw/local', PositionTarget, queue_size=10)
        self.message_sub = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, self.position_callback)
        self.goto_target = PositionTarget()
        self.current_poste = PoseStamped()
        self.seq = 0
        self.start_offboard()
        self.smooth_factor = 0.9
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.target_mask = PositionTarget.IGNORE_VX + PositionTarget.IGNORE_VY + PositionTarget.IGNORE_VZ \
                            + PositionTarget.IGNORE_AFX + PositionTarget.IGNORE_AFY + PositionTarget.IGNORE_AFZ \
                            + PositionTarget.FORCE
        self.mask = self.target_mask

    def publish_position_message(self, x, y, z, mask):
        self.goto_target.header.stamp = rospy.Time.now()
        self.goto_target.header.seq = self.seq
        self.goto_target.coordinate_frame = PositionTarget.FRAME_BODY_OFFSET_NED
        self.goto_target.position.x = x
        self.goto_target.position.y = y
        self.goto_target.position.y = z
        self.goto_target.type_mask = mask
        self.goto_target.yaw = 0
        self.goto_target.yaw_rate = 0
        self.message_pub.publish(self.goto_target)
        self.seq = self.seq + 1

    def position_callback(self, msg):
        self.current_poste = msg

    def position_publish(self):
        self.publish_position_message(self.x, self.y, self.z, self.mask)

    @staticmethod
    def smooth(now, prev, factor):
        return factor * now + (1.0 - factor) * prev

    def warm_position(self, rate):
         for i in range(100):
             p = self.current_poste.pose.position
             self.x = PositionControlNode.smooth(self.x, p.x, self.smooth_factor)
             self.y = PositionControlNode.smooth(self.y, p.y, self.smooth_factor)
             self.z = PositionControlNode.smooth(self.z, p.z, self.smooth_factor)
             self.position_publish()
             rate.sleep()
        
    def run(self):
        rospy.init_node('control_arion', anonymous=True, log_level= rospy.INFO)
        r = rospy.Rate(20)
        self.warm_position(r)
        self.take_control(self.position_publish)
        while not rospy.is_shutdown():
            self.position_publish()
            r.sleep()
        self.release_control()
