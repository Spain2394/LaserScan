#!/usr/bin/env python

"""
ROS node which subscribes to the /scan topic and fits a single line to
this scan, publishing it on the /extracted_lines topic.
"""

import rospy
import math
from fit_line import fit_line

from sensor_msgs.msg import LaserScan
from spain_a2.msg import ExtractedLine
from spain_a2.msg import ExtractedLines

def scan_callback(scan):
    """
    Fit a single line to the given laser scan.

    The line is fitted using scan points that are within 'maximum_range'
    distance (this parameter should be found by the ROS parameter server).  An
    ExtractedLines message is constructed to hold this single line and this
    message is published on /extracted_lines.
    """

    L2 = list()
    total_points = len(scan.ranges)
    endpoints = (0,total_points-1)
    L2.append(endpoints)

    i = 0
    while(i <= len(L2)-1):
	curr_line_points = L2[i]
	curr_line_start = curr_line_points[0]
	curr_line_end = curr_line_points[1]

	line = fit_line(scan,curr_line_start, curr_line_end, maximum_range)
	max_error = 0
	j = curr_line_start + min_points_per_line/2
	max_error_idx = -1
	while ((line is not None) and (j < curr_line_end - min_points_per_line/2 + 1)):

		rho = scan.ranges[j]
		theta = scan.angle_min + scan.angle_increment*j

		error = distance(line.r, line.alpha, rho, theta)
		if error > max_error:
			max_error = error
			max_error_idx = j
		j = j+1

	if max_error > orthog_distance_threshold:
		L2[i] = (curr_line_start, max_error_idx-1)
		L2.insert(i+1, (max_error_idx,curr_line_end))

	#Only increment i if no splitting, if we split we need to
	#reevaluate the new split line at position i
	else:
		i = i +1

		#If we haven't split, merge all the points beyond this one
		if i < len(L2):
			merge_start = L2[i][0]
			merge_end = L2[len(L2)-1][1]
			L2 = L2[:i]
			L2.append((merge_start,merge_end))

    #Build the lines message and publish
    lines = ExtractedLines()
    lines.header.frame_id = scan.header.frame_id #'/base_laser_link'
    for end_points in L2:
	line = fit_line(scan,end_points[0], end_points[1], maximum_range)
	if line is not None:
        	lines.lines.append(line)

    extracted_publisher.publish(lines)

def distance(r, alpha, rho, theta):
	return abs((rho*math.cos(theta-alpha))-r)

if __name__ == '__main__':
    global maximum_range, extracted_publisher, min_points_per_line, orthog_distance_threshold

    # Initialize this node.
    rospy.init_node('extract_all_lines')

    maximum_range = rospy.get_param('maximum_range')
    min_points_per_line = rospy.get_param('min_points_per_line')
    orthog_distance_threshold = rospy.get_param('orthog_distance_threshold')

    #scan_topic = rospy.get_param('~scan_topic')
    #extracted_lines_topic = rospy.get_param('~extracted_lines_topic')
    #print "scan_topic: {}".format(scan_topic)
    #print "extracted_lines_topic: {}".format(extracted_lines_topic)

    "maximum_range: {}".format(maximum_range)
    "min_points_per_line: {}".format(min_points_per_line)
    "orthog_distance_threshold: {}".format(orthog_distance_threshold)

    rospy.Subscriber('/base_scan', LaserScan, scan_callback)
    

    extracted_publisher = rospy.Publisher('/extracted_lines', ExtractedLines, queue_size=1)

    rospy.spin()

