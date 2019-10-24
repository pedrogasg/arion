from geometry_msgs.msg import Point

def smooth(now, prev, factor):
        return factor * now + (1.0 - factor) * prev


def point(x = 0.0, y=0.0, z=0.0):
    p = Point()
    p.x = x
    p.y = y
    p.z = z
    return p