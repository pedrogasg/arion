#!/usr/bin/env python3
import rospy
from arion.offboard import OffboardControl
from arion.point_subscriber import PointSubscriber
from arion.position_subscriber import CurrentPositionSubscriber
from geometry_msgs.msg import PoseStamped

class PositionControlNode(OffboardControl, CurrentPositionSubscriber, PointSubscriber):

    def __init__(self):
        topic_in = rospy.get_param('~raw_point_topic', '/arion/position_point')
        self.rate = rospy.get_param('~raw_point_rate', 20)
        self.message_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
        self.target_position = PoseStamped()
        self.seq = 0
        self.start_point(topic_in)
        self.start_offboard()
        self.start_current_position()
        self.smooth_factor = 0.9

    def publish_position_message(self):
        self.target_position.header.stamp = rospy.Time.now()
        self.target_position.header.seq = self.seq
        self.target_position.pose.position = self.p
        self.message_pub.publish(self.target_position)
        self.seq = self.seq + 1

    def warm_position(self, rate):
         for i in range(100):
             p = self.current_position.pose.position
             self.smooth_point(p.x, p.y, p.z, self.smooth_factor)
             self.publish_position_message()
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
