#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rosbag
import argparse
import jsonlines
from datetime import datetime
from mavros_msgs.msg import RCIn


def main():
    parser = argparse.ArgumentParser(description="Extract rc in data from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("rc_topic", help="rc topic topic.")
    args = parser.parse_args()

    print "Extract images from %s on topic %s into %s" % (args.bag_file,
                                                          args.rc_topic, args.output_dir)

    bag = rosbag.Bag(args.bag_file, "r")
    jsonwriter = jsonlines.open(os.path.join(args.output_dir,"json_data.json"), mode='w')
    for _, msg, _ in bag.read_messages(topics=[args.rc_topic]):
        
        h = msg.header
        secs =  h.stamp.secs + (h.stamp.nsecs / 1000000000.0)
        stearing = msg.channels[1]
        throttle = msg.channels[0]
        obj = {
            "timestamp": secs,
            "stearing": stearing,
            "throttle": throttle
        }
        jsonwriter.write(obj)
    jsonwriter.close()
    bag.close()

    return
if __name__ == '__main__':
    main()