#!/usr/bin/env python3
import rospy
from arion.offboard import OffboardControl
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point

class PositionControlNode(OffboardControl):

    def __init__(self):
        self.message_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)
        self.message_sub = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, self.position_callback)
        self.go_to_pose = PoseStamped()
        self.current_poste = PoseStamped()
        self.seq = 0
        self.start_offboard()
        self.smooth_factor = 0.9
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def publish_position_message(self, x, y, z):
        self.go_to_pose.header.stamp = rospy.Time.now()
        self.go_to_pose.position.x = x
        self.go_to_pose.position.y = y
        self.go_to_pose.position.y = z
        self.message_pub.publish(self.go_to_pose)
        self.seq = self.seq + 1

    def position_callback(self, msg):
        self.current_poste = msg

    def position_publish():
        self.publish_position_message(self.x, self.y, self.z)

    def smooth(now, prev, factor):
        return factor * now + (1.0 - factor) * prev

    def warm_position(self, rate):
         for i in range(100):
             p = self.current_poste.position
             self.x = smooth(self.x, p.x, self.smooth_factor)
             self.y = smooth(self.y, p.y, self.smooth_factor)
             self.z = smooth(self.z, p.z, self.smooth_factor)
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
