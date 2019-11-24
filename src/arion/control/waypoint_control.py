import rospy

from geometry_msgs.msg import Point

from arion.tools import point, distance2D

from arion.subscriber.state_subscriber import State2DSubscriber

class WaypointControl(State2DSubscriber):

    def start_waypoint(self):
        filepath = rospy.get_param('~waypoint_file', '')
        self.loop =  rospy.get_param('~loop', False)
        self.distance = rospy.get_param('~distance', 0.40)
        self.waypoints = list()
        with open(filepath) as fp:
            for line in fp:
                waypoints.append(tuple(map(lambda x: float(x), line.split(','))))
        self.start_2d_state(self.state_update)
        self.started = False
        self.at_destination = False
        self.current_waypoint = self.get_next_waypoint()
        self.started = True

    def state_update(self):
        if self.started and not self.at_destination and self.distance < self.get_distance():
            if len(self.waypoints) > 0 :
                self.current_waypoint = self.get_next_waypoint()
            else :
                self.at_destination = True
                
    def get_next_waypoint(self):
        cw = self.waypoints.pop()
        if self.loop:
            self.waypoints.insert(0, cw)
        return point(cw[0],cw[1],0)

    def get_distance(self):
        return distance2D(self.state.x, self.state.y, self.current_waypoint.x, self.current_waypoint.y)

        
