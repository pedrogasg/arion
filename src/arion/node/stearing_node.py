import rospy
import numpy as np
from std_msgs.msg import Float32
from arion.camera import GStreamerCamera
from arion.prediction import CropResizedGradientLayer, Predictor

class StearingNode:
    def __init__(self):

        rospy.init_node('prediction_arion', anonymous=True, log_level= rospy.INFO)
        model_path = rospy.get_param('~prediction_model_path', '/home/jetson/test/cat_model5_s2_end.h5')
        topic_out = rospy.get_param('~prediction_out_topic', '/arion/stearing')
        width = rospy.get_param('~prediction_witdh', 320)
        height = rospy.get_param('~prediction_height', 180)
        rate = rospy.get_param('~prediction_rate', 30)
        self.cam = GStreamerCamera(src=0, width=width, height=height, rate=rate)
        self.model = Predictor(model_path, 9)
        self.pub = rospy.Publisher(topic_out, Float32, queue_size=1)
        self.predicting = False
        self.frame = np.empty((self.height, self.width, 3), dtype=np.uint8)

    def update_image(self, change):
        if self.predicting:
            return
        self.frame = change['new'].copy()


    def run(self):
        self.cam.running = True
        self.cam.observe(self.update_image, names='value')
        r =rospy.Rate(30)
        while not rospy.is_shutdown():
            self.predicting = True    
            p = self.model.call(self.frame)
            self.predicting = False
            self.pub.publish(p)
            r.sleep()
            
        self.cam.running = False