import rospy
from std_msgs.msg import Float32
from arion.camera import GStreamerCamera
from arion.prediction import CropResizedGradientLayer, Predictor

class StearingNode:
    def __init__(self):

        rospy.init_node('prediction_arion', anonymous=True, log_level= rospy.INFO)
        model_path = rospy.get_param('~prediction_model_path', '/home/jetson/test/cat_model5_s2_end.h5')
        topic_out = rospy.get_param('~prediction_out_topic', '/arion/stearing')
        
        self.rate = rospy.get_param('~prediction_rate', 30)
        self.cam = GStreamerCamera(src=0, width=410, height=308)
        self.model = Predictor(model_path, 9, custom_objects={'CropResizedGradientLayer': CropResizedGradientLayer})
        self.pub = rospy.Publisher(topic_out, Float32, queue_size=1)


    def run(self):
        r =rospy.Rate(self.rate)
        self.cam.start()
        while not rospy.is_shutdown():
            _, frame = self.cam.read()
            p = self.model.call(frame)
            self.pub.publish(p)
            r.sleep()
        self.cam.stop()