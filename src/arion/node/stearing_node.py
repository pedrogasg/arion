import rospy
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

    def update_image(self, change):
        if self.predicting:
            return
        self.predicting = True    
        p = self.model.call(change['new'])
        self.predicting = False
        self.pub.publish(p)

    def run(self):
        self.cam.running = True
        self.cam.observe(self.update_image, names='value')
        rospy.spin()
        self.cam.running = False
        r =rospy.Rate(self.rate)
        self.cam.start()
        self.cam.stop()