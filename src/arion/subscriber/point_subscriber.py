import rospy
from geometry_msgs.msg import Point
from arion.tools import point, smooth

class PointSubscriber:
    def start_point(self, topic):
        self.p = point()
        self.point_sub = rospy.Subscriber(topic, Point, self.update_point)

    def update_point(self, p):
        self.p = p

    def smooth_point(self, x, y, z, smooth_factor):
        self.p.x = smooth(self.p.x, x, smooth_factor)
        self.p.y = smooth(self.p.y, y, smooth_factor)
        self.p.z = smooth(self.p.z, z, smooth_factor)