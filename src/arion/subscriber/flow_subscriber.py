import rospy
from mavros_msgs.msg import OpticalFlowRad

class PX4FlowSubscriber:
    def start_optical_flow(self, topic):
        self.flow_rad = OpticalFlowRad()
        self.flow_rad_sub = rospy.Subscriber(topic, OpticalFlowRad, self.update_optical_flow)

    def update_optical_flow(self, rad):
        self.flow_rad = rad
