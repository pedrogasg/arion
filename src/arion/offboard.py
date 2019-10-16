import rospy
import time
from mavros_msgs.srv import CommandBool, SetMode

class OffboardControl:

    def start_offboard(self):
        self.armService = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        self.flightModeService = rospy.ServiceProxy('/mavros/set_mode', SetMode)

    def manual(self):
        set_mode()    

    def offboard(self):
        return self.set_mode('OFFBOARD')

    def set_mode(self, mode="MANUAL"):
        if self.flightModeService(custom_mode=mode):
            rospy.loginfo("Vehicle is now in %s mode" % mode)
            return True
        else:
            rospy.loginfo("Vehicle %s failed" % mode)
            return False

    def arm(self):
        if self.armService(True):
            rospy.loginfo("Vehicle is now armed!")
            return True
        else:
            rospy.loginfo("Vehicle arming failed!")
            return False

    def disarm(self):
        if self.armService(False):
            rospy.loginfo("Vehicle disarmed!")
            return True
        else:
            rospy.loginfo("Vehicle disarming failed!")
            return False
    
    def take_control(self, callback):
        for i in range(10):
            callback()
            self.arm()
            self.offboard()
            rospy.loginfo("%d" % i)
            time.sleep(0.2)

    def release_control(self, callback):
        callback()
        while not self.disarm() and not self.manual():
            callback()
            time.sleep(0.2)