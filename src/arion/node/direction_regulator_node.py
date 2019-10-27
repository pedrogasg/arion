import rospy
import numpy as np

from geometry_msgs.msg import Point

from mavros_msgs.msg import ActuatorControl

from arion.offboard import OffboardControl
from arion.subscriber.rc_subscriber import RCSubscriber
from arion.subscriber.state_subscriber import State2DSubscriber
from arion.tools import _RC_THOTTLE_, _RC_STEARING_, _ACTUATORS_, _THOTTLE_, _STEARING_, map_from_pwm

class DirectionRegulatorNode(RCSubscriber, State2DSubscriber, OffboardControl):

    def __init__(self):
        self.seq = 0
        self.throtle = 0.0
        self.steering = 0.0
        self.rate = rospy.get_param('~regulator_rate', 20)
        self.message_pub = rospy.Publisher('/mavros/actuator_control', ActuatorControl, queue_size=1)
        self.state_pub = rospy.Publisher('/arion/state', Point, queue_size=1)
        self.actuator_control_message = ActuatorControl()
        self.start_offboard()
        self.start_2d_state()
        self.start_rc()
        self.inputs = np.zeros(_ACTUATORS_)

    def update_rc(self, rc):
        self.throtle = map_from_pwm(rc.channels[_RC_THOTTLE_])
        self.steering = map_from_pwm(rc.channels[_RC_STEARING_])

    def publish_actuator_message(self):
        self.inputs[_THOTTLE_] = self.throtle
        self.inputs[_STEARING_] = self.steering
        self.actuator_control_message.header.stamp = rospy.Time.now()
        self.actuator_control_message.header.seq = self.seq
        self.actuator_control_message.group_mix = ActuatorControl.PX4_MIX_FLIGHT_CONTROL
        self.actuator_control_message.controls = self.inputs
        self.message_pub.publish(self.actuator_control_message)
        self.seq = self.seq + 1
        self.state_pub.publish(self.state)


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
