import rospy
import numpy as np
from arion.yaw_control import YawControl
from arion.speed_control import SpeedControl
from arion.offboard import OffboardControl
from mavros_msgs.msg import ActuatorControl

class ActuatorControlNode(OffboardControl, YawControl, SpeedControl):
    _ACTUATORS_ = 8
    _THOTTLE_ = 3
    _STEARING_ = 3

    def __init__(self):
        self.message_pub = rospy.Publisher('/mavros/actuator_control', ActuatorControl, queue_size=1)
        self.actuator_control_message = ActuatorControl()
        self.seq = 0
        self.start_offboard()
        self.start_throttle()
        self.start_stearing()

    def publish_actuator_message(self, inputs):
        self.actuator_control_message.header.stamp = rospy.Time.now()
        self.actuator_control_message.header.seq = self.seq
        self.actuator_control_message.group_mix = self.actuator_control_message.PX4_MIX_FLIGHT_CONTROL
        self.actuator_control_message.controls = inputs
        self.message_pub.publish(self.actuator_control_message)
        self.seq = self.seq + 1
        
    def run(self):
        rospy.init_node('control_arion', anonymous=True, log_level= rospy.INFO)
        r =rospy.Rate(240)

        inputs = np.zeros(_ACTUATORS_)

        self.take_control(lambda: self.publish_actuator_message(inputs))
            
        while not rospy.is_shutdown():
            inputs[_THOTTLE_] = self.throttle
            inputs[_STEARING_] = self.stearing
            self.publish_actuator_message(inputs)

            r.sleep()
        inputs[_THOTTLE_] = self.throttle
        inputs[_STEARING_] = self.stearing

        self.release_control(lambda: self.publish_actuator_message(inputs))
