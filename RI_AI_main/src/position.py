import math
import rospy
from geometry_msgs.msg import Pose2D

def main(robot_info,geometry):
	#print(robot_info)
	length_devide=geometry.field_length/8
	width_devide=geometry.field_width/3
	position=0
	robot_position_x=robot_info.pose.x+6
	robot_position_y=robot_info.pose.y+4.5

	for i in range(8):
		if robot_position_x>=length_devide*i and robot_position_x<=length_devide*(i+1):
			for h in range(3):
				if robot_position_y>=width_devide*h and robot_position_y<=width_devide*(h+1):
					position=i+(h*8)
					break

	return position 

def line_limit(position,geometry):

	if position.x>=geometry.field_length/2:
		position.x=geometry.field_length/2
	if position.x<=-geometry.field_length/2:
		position.x=-geometry.field_length/2
	if position.y>=geometry.field_width/2:
		position.y=geometry.field_width/2
	if position.y<=-geometry.field_width/2:
		position.y=-geometry.field_width/2

	return position


