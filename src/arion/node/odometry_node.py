import rospy
from arion.position import VisionOdometer
from nav_msgs.msg import Odometry

class OdometryNode:
    def __init__(self):
        rospy.init_node('odometry_test', anonymous=True, log_level= rospy.INFO)

        topic_in = rospy.get_param('~input_topic', '/camera/odom/sample')
        topic_out = rospy.get_param('~output_topic', '/mavros/odometry/out')
        
        self.rate= rospy.get_param('~output_rate', 30)

        self.odometer = VisionOdometer(topic_in)
        self.pub = rospy.Publisher(topic_out, Odometry, queue_size=1)


    def run(self):
        r =rospy.Rate(self.rate)

        while not rospy.is_shutdown():
            odom = self.odometer.read()
            if odom is not None:
                self.pub.publish(odom)
            r.sleep()
