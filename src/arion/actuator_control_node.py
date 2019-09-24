#!/usr/bin/env python3
import rospy
import numpy as np
from arion import YawControl, SpeedControl
from mavros_msgs.msg import ActuatorControl

class ActuatorControlNode(YawControl, SpeedControl):

    def __init__(self):
        self.message_pub = rospy.Publisher("/mavros/actuator_control", ActuatorControl, queue_size=1)
        self.actuator_control_message = ActuatorControl()
        self.seq = 0
        
    def run(self):
        rospy.init_node('control_test', anonymous=True, log_level= rospy.INFO)
        r =rospy.Rate(240)
                           #    #    yaw            trhottle
        inputs = np.array((0.0, 0.0, self.stearing, self.trhottle, 0.0, 0.0, 0.0, 0.0))
        
        while not rospy.is_shutdown():
            self.actuator_control_message.header.stamp = rospy.Time.now()
            self.actuator_control_message.header.seq = self.seq
            self.actuator_control_message.group_mix = self.actuator_control_message.PX4_MIX_FLIGHT_CONTROL
            inputs[3] = self.trhottle
            inputs[2] = self.stearing
            self.actuator_control_message.controls = inputs
            self.message_pub.publish(self.actuator_control_message)
            self.seq = self.seq + 1
            r.sleep()
