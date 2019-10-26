import rospy
from arion.subscriber.flow_subscriber import PX4FlowSubscriber

class WheelEncoderNode(PX4FlowSubscriber):
    def __init__(self):
        self.rate = rospy.get_param('~wheel_raw_point_rate', 20)
        topic_flow = rospy.get_param('~optical_flow_topic', '/mavros/px4flow/raw/optical_flow_rad')
        self.start_optical_flow(topic_flow)


    def run():
        r = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            rospy.loginfo(self.flow_rad)
            r.sleep()
