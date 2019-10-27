import rospy
import numpy as np
from mavros_msgs.msg import ActuatorControl

from arion.offboard import OffboardControl
from arion.subscriber.rc_subscriber import RCSubscriber
from arion.subscriber.position_subscriber import CurrentPositionSubscriber


class DirectionRegulatorNode(RCSubscriber, CurrentPositionSubscriber, OffboardControl):

    def __init__(self):
        self.rate = rospy.get_param('~regulator_rate', 20)
        self.message_pub = rospy.Publisher('/mavros/actuator_control', ActuatorControl, queue_size=1)
        self.actuator_control_message = ActuatorControl()
        self.start_offboard()
        self.start_current_position()
        self.start_rc()

    def publish_actuator_message(self):
        self.actuator_control_message.header.stamp = rospy.Time.now()
        self.actuator_control_message.header.seq = self.seq
        self.actuator_control_message.group_mix = ActuatorControl.PX4_MIX_FLIGHT_CONTROL
        self.actuator_control_message.controls = (self.channels / RCSubscriber._ZERO_) - 1
        self.message_pub.publish(self.actuator_control_message)
        self.seq = self.seq + 1

    def warm_position(self, rate):
         for i in range(100):
             self.publish_actuator_message()
             rate.sleep()

    def run(self):
        rospy.init_node('regulator_arion', anonymous=True, log_level= rospy.INFO)
        r = rospy.Rate(self.rate)
        self.warm_position(r)
        self.take_control(self.publish_actuator_message)
        while not rospy.is_shutdown():
            self.publish_actuator_message()
            r.sleep()
        self.release_control()
