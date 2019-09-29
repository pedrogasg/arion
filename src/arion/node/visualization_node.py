import math
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA

class NavPath:

    def __init__(self, threshold):
        self._path = []
        self.threshold = threshold

    @staticmethod 
    def distance(p1, p2):
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        dz = p1.z - p2.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def callback(self, msg):
        point = msg.pose.pose.position
        if (len(self._path) == 0 or
                NavPath.distance(self._path[-1], point) > self.threshold):
            self._path.append(point)

    def get_path(self):
        return Marker(
            type=Marker.LINE_STRIP,
            ns='path',
            id=len(self._path),
            points=self._path,
            scale=Vector3(0.05, 0.05, 0.05),
            header=Header(frame_id='map'),
            color=ColorRGBA(0, 1.0, 0, 1.0))

class VisualiZationNode:
    def __init__(self):
        rospy.init_node('visualization_test', anonymous=True, log_level= rospy.INFO)
        self.nav_path = NavPath(0.3)
        self.pub = rospy.Publisher('arion/visualization_marker', Marker, queue_size=5)
        self.sub =rospy.Subscriber('/mavros/odometry/in', Odometry, self.nav_path.callback)
        
    def run(self):
        r =rospy.Rate(30)
        while not rospy.is_shutdown():
            p = self.nav_path.get_path()
            self.pub.publish(p)
            r.sleep()