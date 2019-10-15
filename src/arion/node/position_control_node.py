#!/usr/bin/env python3
import rospy
from arion.offboard import OffboardControl
from mavros_msgs.msg import PositionTarget

class PositionControlNode(OffboardControl):

    def __init__(self):
        self.message_pub = rospy.Publisher('mavros/setpoint_raw/local', PositionTarget, queue_size=1)
        self.position_target_message = PositionTarget()
        self.seq = 0
        self.start_offboard()

    def publish_position_message(self, x, y, z, yaw, yaw_rate=1):
        self.position_target_message.header.stamp = rospy.Time.now()
        self.position_target_message.position.x = x
        self.position_target_message.position.y = y
        self.position_target_message.position.z = z
        self.position_target_message.type_mask = PositionTarget.IGNORE_VX + PositionTarget.IGNORE_VY + PositionTarget.IGNORE_VZ \
                                    + PositionTarget.IGNORE_AFX + PositionTarget.IGNORE_AFY + PositionTarget.IGNORE_AFZ \
                                    + PositionTarget.FORCE
        self.position_target_message.coordinate_frame = PositionTarget.FRAME_BODY_OFFSET_NED
        self.message_pub.publish(self.position_target_message)
        self.position_target_message.yaw = yaw
        self.position_target_message.yaw_rate = yaw_rate
        self.seq = self.seq + 1
        
    def run(self):
        rospy.init_node('control_arion', anonymous=True, log_level= rospy.INFO)

        self.take_control(lambda: self.publish_position_message(0,0,0,0))
        rospy.spin()
        self.release_control(lambda: self.publish_position_message(0,0,0,0))
