#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2
import rosbag
import argparse
import jsonlines
import numpy as np
from datetime import datetime
from sensor_msgs.msg import CompressedImage

def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images data from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("image_topic", help="Image topic.")
    parser.add_argument("--i", nargs="?", const=True, default=False, dest="invert")

    args = parser.parse_args()

    print "Extract images from %s on topic %s into %s" % (args.bag_file,
                                                          args.image_topic, args.output_dir)

    bag = rosbag.Bag(args.bag_file, "r")
    count = 0
    jsonwriter = jsonlines.open(os.path.join(args.output_dir,"json_data.json"), mode='w')
    for _, msg, _ in bag.read_messages(topics=[args.image_topic]):
        
        h = msg.header
        np_arr = np.fromstring(msg.data, np.uint8)
        cv_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        secs =  h.stamp.secs + (h.stamp.nsecs / 1000000000.0)
        d = datetime.fromtimestamp(secs).strftime("%Y_%m_%d_%H_%M_%S_%f")
        (h, w) = cv_img.shape[:2]
        if args.invert:
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, 180, 1.0)
            cv_img = cv2.warpAffine(cv_img, M, (w, h))
        obj = {
            "timestamp": secs,
            "filename": "%s.jpg" % d,
            "height": h,
            "width": w,
            "source": args.image_topic
        }
        jsonwriter.write(obj)
        cv2.imwrite(os.path.join(args.output_dir, "%s.jpg" % d), cv_img)
        
        count += 1

    jsonwriter.close()
    bag.close()
    print "The exporter wrote %i images" % count

    return

if __name__ == '__main__':
    main()