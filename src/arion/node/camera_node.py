
import rospy
import numpy as np
from arion.camera import GStreamerCamera
from sensor_msgs.msg import CompressedImage

class CameraNode:
    def __init__(self):

        rospy.init_node('camera_arion', anonymous=True, log_level= rospy.INFO)
        topic_out = rospy.get_param('~camera_out_topic', '/arion/image_compressed')
        
        self.rate = rospy.get_param('~camera_rate', 30)
        self.cam = GStreamerCamera(src=0, width=410, height=308)
        self.pub = rospy.Publisher(topic_out, CompressedImage, queue_size=1)


    def run(self):
        r =rospy.Rate(self.rate)
        self.cam.start()
        while not rospy.is_shutdown():
            _, frame = self.cam.read()

            #### Create CompressedIamge ####
            msg = CompressedImage()
            msg.header.stamp = rospy.Time.now()
            msg.format = "jpeg"
            msg.data = np.array(GStreamerCamera.encode_image(frame)[1]).tostring()

           # Publish new image
            self.pub.publish(msg)
            r.sleep()
        self.cam.stop()