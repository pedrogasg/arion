import rospy

from mavros_msgs.msg import PositionTarget
from geometry_msgs.msg import PoseStamped, Point

from arion.offboard import OffboardControl
from arion.subscriber.point_subscriber import PointSubscriber
from arion.subscriber.position_subscriber import CurrentPositionSubscriber

class PositionControlRawNode(OffboardControl, CurrentPositionSubscriber, PointSubscriber):

    LOITER = 12288
    def __init__(self):
        topic_in = rospy.get_param('~raw_point_topic', '/arion/raw_point')
        self.rate = rospy.get_param('~raw_point_rate', 20)
        self.message_pub = rospy.Publisher('mavros/setpoint_raw/local', PositionTarget, queue_size=10)
        self.target_position = PositionTarget()
        self.seq = 1
        self.start_point(topic_in)
        self.start_offboard()
        self.start_current_position()
        self.smooth_factor = 0.9
        self.mask = PositionControlRawNode.LOITER

    def publish_position_message(self):
        self.target_position.header.stamp = rospy.Time.now()
        self.target_position.header.seq = self.seq
        self.target_position.header.frame_id = "enu_world"
        self.target_position.coordinate_frame = PositionTarget.FRAME_LOCAL_NED
        self.target_position.position.x = self.p.x
        self.target_position.position.y = self.p.y
        self.target_position.position.z = self.p.z
        self.target_position.type_mask = self.mask
        self.target_position.yaw = 0
        self.target_position.yaw_rate = 1
        self.message_pub.publish(self.target_position)
        self.seq = self.seq + 1

    def warm_position(self, rate):
         for i in range(100):
             p = self.current_position.pose.position
             self.smooth_point(p.x, p.y, p.z, self.smooth_factor)
             self.publish_position_message()
             rate.sleep()
        
    def run(self):
        rospy.init_node('control_arion', anonymous=True, log_level= rospy.INFO)
        r = rospy.Rate(self.rate)
        self.warm_position(r)
        self.take_control(self.publish_position_message)
        while not rospy.is_shutdown():
            self.publish_position_message()
            r.sleep()
        self.release_control()
