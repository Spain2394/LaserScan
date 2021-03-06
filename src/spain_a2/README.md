# spain_a2 
## by Allen Spain
## 10/29/2018

Application of Split-and-Merge Segmentation algorithm 

## To Run display_lines node, and extract_all_lines node
 - run ```roscore``` in ROS environment
 - download spain_a2 and place in ```catkin_ws/src```
 - navigate to your ```catkin_ws```, and run ```$ source devel/setup.bash```
 - navigate to package ```spain_a2``` to play a rosbag run ```$ ./viz``` and enter rosbag name when prompted. 
 - to start nodes run ```$ roslaunch spain_a2 my_extract_all.launch```

## Rosbags
Example rosbags collected using Hokuyo laser scanner in fixed locations rosbags:  
- ```corridor1.bag```
- ```corridor2.bag```
- ```library.bag```
- ```stair.bag```

## Testing
 - run ```roslaunch spain_a2 my_stage_rviz.launch``` to visualize in rviz environment

## Parameters
 - ```maximum_range``` representing the sensors max range
 - ```min_points_per_line``` minimum point required to fit a line
 - ```orthog_distance_threshold``` threshold used in deciding to split a lane
 
## Observations
### Split-and-Merge Segmentation Algorithm
**Split**
  - Involves fitting points in range ```maximum_range```
   with at least ```min_points_per_line```

**Merge**
  - If the the two segments are close enough to obtain a common line, find the outer most point
  - If this point is within the ```orthog_distance_threshold``` then merge the segments creating an edge
  
**Result**
  - Resultant lines are published to a new topic ```extracted_lines``` Composed of a two float32 variables, radius r and angle alpha, for visualization in ```rviz```

**References** 
1. [COMP 4766/6912, Spring 2018](http://www.cs.mun.ca/~av/courses/4766-current/?page_id=84)
2. [COMP 4766/6912, Spring 2018](http://www.cs.mun.ca/~av/courses/4766-current/?page_id=103)


