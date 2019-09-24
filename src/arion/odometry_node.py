import rospy
from arion.position import VisionOdometer


class OdometryNode:
    def __init__(self):
        rospy.init_node('odometry_test', anonymous=True, log_level= rospy.INFO)
        self.odometer = VisionOdometer()


    def run(self):
        r =rospy.Rate(20)
        while not rospy.is_shutdown():
            odom = self.odometer.read()
            rospy.loginfo(odom)
            r.sleep()
