import rospy
from std_msgs.msg import Float32
from arion.camera import GStreamerCamera
from arion.prediction import CropResizedGradientLayer, Predictor

class StearingNode:
    def __init__(self):
        rospy.init_node('prediction_test', anonymous=True, log_level= rospy.INFO)
        self.cam = GStreamerCamera(src=0, width=410, height=308)
        self.model = Predictor('/home/jetson/test/cat_model5_s2_end.h5', 9, custom_objects={'CropResizedGradientLayer': CropResizedGradientLayer})
        self.pub = rospy.Publisher('/prediction/stearing', Float32, queue_size=1)


    def run(self):
        r =rospy.Rate(60)
        self.cam.start()
        while not rospy.is_shutdown():
            _, frame = self.cam.read()
            p = self.model.call(frame)
            self.pub.publish(p)
            r.sleep()
        self.cam.stop()