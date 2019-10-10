
import rospy
import numpy as np
from arion.camera import GStreamerCamera
from sensor_msgs.msg import CompressedImage

class CameraNode:
    def __init__(self):

        rospy.init_node('camera_arion', anonymous=True, log_level= rospy.INFO)
        topic_out = rospy.get_param('~camera_out_topic', '/arion/image_compressed')
        width = rospy.get_param('~camera_witdh', 320)
        height = rospy.get_param('~camera_height', 180)
        rate = rospy.get_param('~camera_rate', 30)
        self.cam = GStreamerCamera(src=0, width=width, height=height, rate=rate)
        self.pub = rospy.Publisher(topic_out, CompressedImage, queue_size=1)

    def update_image(self, change):
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = GStreamerCamera.encode_image(change['new'])
        self.pub.publish(msg)


    def run(self):
        self.cam.running = True
        self.cam.observe(self.update_image, names='value')
        rospy.spin()
        self.cam.running = False