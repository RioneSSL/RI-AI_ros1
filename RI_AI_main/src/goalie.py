import rospy
import math
import calculate
from geometry_msgs.msg import Pose2D
from RI_AI_msg.msg import SEND,Flag

def main(our_goal_info,goalie,ball_info,geometry):
	send_val=SEND()

	OUR_goal_position_middle = Pose2D(-geometry.field_length/2,0,0)
	target_position=Pose2D(OUR_goal_position_middle.x+0.2,ball_info.pose.y,0)

	flag=False
	if goalie.pose.y>=geometry.goal_width/2:
		target_position.y=geometry.goal_width/2
		flag=True
	
	if goalie.pose.y<=-geometry.goal_width/2:
		target_position.y=-geometry.goal_width/2
		flag=True

	OUR_goal_robot=calculate.Calc(our_goal_info,goalie.pose)
	OUR_goal_robot_degree=OUR_goal_robot.degree_calc() - math.degrees(goalie.pose.theta) +180
	OUR_goal_robot_distance=OUR_goal_robot.distance_calc()

	robot_ball_info=calculate.Calc(goalie.pose,ball_info.pose)
	robot_ball_degree=robot_ball_info.degree_calc() - math.degrees(goalie.pose.theta) +180
	robot_ball_distance=robot_ball_info.distance_calc()

	robot_ball_degree = calculate.degree_improve(robot_ball_degree)
	OUR_goal_robot_degree = calculate.degree_improve(OUR_goal_robot_degree)

	target_info=calculate.Calc(target_position,goalie.pose)
	target_degree=target_info.degree_calc() - goalie.pose.theta*180/3.14 
	target_degree=calculate.degree_improve(target_degree)

	kick_pow_x=0.0
	#target_degree=

	send_val.stop=False
	send_val.direction=math.degrees(goalie.pose.theta)
	send_val.direction=calculate.degree_improve(send_val.direction)
	send_val.direction=math.radians(-send_val.direction)
	send_val.move_degree=math.radians(target_degree)
	send_val.spinner=True
	send_val.kickspeedx=OUR_goal_robot_distance
	send_val.distance=math.fabs(math.radians(robot_ball_degree))
	if flag==True:
		send_val.distance=0.1
	send_val.robot_id=goalie.robot_id

	return send_val
