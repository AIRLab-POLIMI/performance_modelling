#!/usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import glob
import os
import sys
from os import path
import rosbag
from performance_modelling_py.utils import print_info, print_error


def save_laser_scan_msgs(bag_file_path, scans_file_path, topic_name):
    if not path.exists(bag_file_path):
        print_error("file not found: {}".format(bag_file_path))
        return

    scans_file_dir = path.dirname(scans_file_path)
    if not path.exists(scans_file_dir):
        os.makedirs(scans_file_dir)

    bag = rosbag.Bag(bag_file_path)

    with open(scans_file_path, 'w') as scans_file:
        for _, laser_scan_msg, _ in bag.read_messages(topics=[topic_name]):
            scans_file.write("{t}, {angle_min}, {angle_max}, {angle_increment}, {range_min}, {range_max}, {ranges}\n".format(
                t=laser_scan_msg.header.stamp.to_sec(),
                angle_min=laser_scan_msg.angle_min,
                angle_max=laser_scan_msg.angle_max,
                angle_increment=laser_scan_msg.angle_increment,
                range_min=laser_scan_msg.range_min,
                range_max=laser_scan_msg.range_max,
                ranges=', '.join(map(str, laser_scan_msg.ranges))))

    bag.close()


if __name__ == '__main__':
    print_info("Python version:", sys.version_info)
    default_base_run_folder = "~/ds/performance_modelling/output/test_slam/*"
    default_scans_file_name = "scans_gt.csv"
    default_topic_name = "/scan_gt"

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='Extracts laser scan messages from ros bags for each run and writes to a csv file.')

    parser.add_argument('-r', dest='base_run_folder',
                        help='Folder in which the result of each run will be placed. Defaults to {}.'.format(default_base_run_folder),
                        type=str,
                        default=default_base_run_folder,
                        required=False)

    parser.add_argument('-o', dest='scans_file_name',
                        help='Filename of the output laser scan csv. Defaults to {}'.format(default_scans_file_name),
                        type=str,
                        default=default_scans_file_name,
                        required=False)

    parser.add_argument('-t', dest='topic_name',
                        help='Topic name for which laser scan messages are extracted. Defaults to {}.'.format(default_topic_name),
                        type=str,
                        default=default_topic_name,
                        required=False)

    args = parser.parse_args()

    run_folders = list(filter(path.isdir, glob.glob(path.expanduser(args.base_run_folder))))
    for progress, run_folder in enumerate(run_folders):
        print_info("main: save_laser_scan_msgs {:3d}% {}".format(int((progress + 1)*100/len(run_folders)), run_folder))
        bag_path = path.join(run_folder, "benchmark_data.bag")
        scans_path = path.join(run_folder, "benchmark_data", args.scans_file_name)
        save_laser_scan_msgs(bag_path, scans_path, args.topic_name)
