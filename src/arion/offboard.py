import rospy
from mavros_msgs.srv import CommandBool, SetMode

class OffboardControl:

    def start_offboard(self):
        self.armService = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        self.flightModeService = rospy.ServiceProxy('/mavros/set_mode', SetMode)

    def manual(self):
        set_mode()    

    def offboard(self):
        return set_mode('OFFBOARD')

    def set_mode(self, mode="MANUAL"):
        if self.flightModeService(custom_mode=mode):
            return True
        else:
            print("Vechile %s failed" %mode)
            return False

    def arm(self):
        if self.armService(True):
            return True
        else:
            print("Vehicle arming failed!")
            return False

    def disarm(self):
        if self.armService(False):
            return True
        else:
            print("Vehicle disarming failed!")
            return False
    
    def take_control(self, callback):
        callback()
        while not self.arm() and not self.offboard():
            callback()
            time.sleep(0.2)

    def release_control(self, callback):
        callback()
        while not self.disarm() and not self.manual():
            callback()
            time.sleep(0.2)