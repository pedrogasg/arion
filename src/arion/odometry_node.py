import rospy
from arion.position import VisionOdometer


class OdometryNode:
    def __init__(self):
        rospy.init_node('odometry_test', anonymous=True, log_level= rospy.INFO)
        self.odometer = VisionOdometer()


    def run(self):
        r =rospy.Rate(10)
        d_x, d_y, d_z = 0, 0, 0
        o_x, o_y, o_z = 0, 0, 0

        while not self.odometer.is_started:
            r.sleep()

        while not rospy.is_shutdown():
            odom = self.odometer.read()
            pos = odom.pose.pose.position
            d_x = d_x + o_x + pos.x
            o_x = pos.x
            d_y = d_y + o_y + pos.y
            o_y = pos.y
            d_z = d_z + o_z + pos.z
            o_z = pos.z
            rospy.loginfo("distance in x = %d, y = %d, z = %d" % (d_x, d_y, d_z))
            r.sleep()
