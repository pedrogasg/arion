from geometry_msgs.msg import Point

_PWM_MAX_ = 2006
_PWM_ZERO_ = 1494
_PWM_MIN_ = 982

_MAX_ = 1
_MIN_ = -1

_RC_THOTTLE_ = 0
_RC_STEARING_ = 1

_THOTTLE_ = 3
_STEARING_ = 2

_ACTUATORS_ = 8

def smooth(now, prev, factor):
    return factor * now + (1.0 - factor) * prev


def point(x = 0.0, y=0.0, z=0.0):
    p = Point()
    p.x = x
    p.y = y
    p.z = z
    return p

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def map_from_pwm(x):
    return map(x, _PWM_MIN_, _PWM_MAX_, _MIN_, _MAX_)

def distance2D(x1, y1, x2, y2):
    ((x2 - x1) ** 2.0 + (y2 - y1) ** 2.0) ** (0.5)