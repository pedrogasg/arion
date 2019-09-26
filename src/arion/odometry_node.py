import rospy
from arion.position import VisionOdometer
from nav_msgs.msg import Odometry

class OdometryNode:
    def __init__(self):
        rospy.init_node('odometry_test', anonymous=True, log_level= rospy.INFO)
        self.odometer = VisionOdometer()
        self.pub = rospy.Publisher('/mavros/odometry/out', Odometry, queue_size=1)


    def run(self):
        r =rospy.Rate(30)

        while not rospy.is_shutdown():
            odom = self.odometer.read()
            if odom is not None:
                rospy.loginfo(odom.header.frame_id)
                rospy.loginfo(odom.child_frame_id)
                self.pub.publish(odom)
            r.sleep()
