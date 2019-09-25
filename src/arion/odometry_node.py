import rospy
import tf2_ros
from arion.position import VisionOdometer
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion, Point
from transformations import quaternion_multiply


class OdometryNode:
    def __init__(self):
        rospy.init_node('odometry_test', anonymous=True, log_level= rospy.INFO)
        self.odometer = VisionOdometer()
        self.pub = rospy.Publisher('mavros/vision_pose/pose', PoseStamped, queue_size=1)
        self.tf_buffer = tf2_ros.Buffer()
        self.pose = PoseStamped()




    def to_wxyz(self, quaternion):
        return [quaternion.w,
                quaternion.x,
                quaternion.y,
                quaternion.z]


    def to_quaternion(self, array):
        return Quaternion(array[1], array[2], array[3], array[0])


    def rotate(self, quaternion, rotation):
        q_orig = self.to_wxyz(quaternion)
        q_rot = self.to_wxyz(rotation)
        q_new = self.quaternion_multiply(q_rot, q_orig)
        return self.to_quaternion(q_new)


    def translate(self, point, translation):
        x = point.x + translation.x
        y = point.y + translation.y
        z = point.z + translation.z
        return Point(x, y, z)


    def run(self):
        
        tf2_ros.TransformListener(self.tf_buffer)
        time_zero = rospy.Time(0)
        r =rospy.Rate(10)
        d_x, d_y, d_z = 0, 0, 0
        o_x, o_y, o_z = 0, 0, 0

        while not rospy.is_shutdown():
            odom = self.odometer.read()
            if odom is not None:
                trans = self.tf_buffer.lookup_transform('local_origin', 'camera_odom_frame', time_zero)
                transform = trans.transform

                pose = odom.pose.pose

                q = self.rotate(pose.orientation, transform.rotation)
                point = self.translate(pose.position, transform.translation)

                # swap x and y
                point.x, point.y = point.y, point.x
                # invert x
                point.x = - point.x
                self.pose.header.stamp = rospy.Time.now()
                self.pose.pose.position = point
                self.pose.orientation = q

                rospy.loginfo(self.pose)
            r.sleep()
