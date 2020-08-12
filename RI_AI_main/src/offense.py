import math
import rospy
import calculate
import position
from geometry_msgs.msg import Pose2D
from RI_AI_msg.msg import SEND,Flag

def main(TH_goal_info,attacker,offense,ball_info,geometry):
	send_val=SEND()

	AT_TH_info=calculate.Calc(attacker.pose,TH_goal_info)
	AT_TH_distance=AT_TH_info.distance_calc()
	AT_TH_degree=AT_TH_info.degree_calc()
	AT_TH_degree=calculate.degree_improve(AT_TH_degree)

	AT_OFF_info=calculate.Calc(attacker.pose, offense.pose)
	AT_OFF_degree=AT_OFF_info.degree_calc()-math.degrees(offense.pose.theta)
	AT_OFF_distance=AT_OFF_info.distance_calc()
	AT_OFF_degree=calculate.degree_improve(AT_OFF_degree)

	target_position=Pose2D(attacker.pose.x+math.cos(attacker.pose.theta)*AT_TH_distance/2, attacker.pose.y+math.sin(attacker.pose.theta)*AT_TH_distance/2,0)
	target_robot_info=calculate.Calc(target_position,offense.pose)
	target_robot_distance=target_robot_info.distance_calc()
	target_robot_degree=target_robot_info.degree_calc()-math.degrees(offense.pose.theta)
	target_robot_degree=calculate.degree_improve(target_robot_degree)
	
	send_val.stop=False
	send_val.direction=math.radians(AT_OFF_degree)
	send_val.move_degree=math.radians(target_robot_degree)
	send_val.spinner=False
	send_val.kickspeedx=0
	send_val.distance=target_robot_distance
	if send_val.distance>=1:
		send_val.distance=1
	send_val.robot_id=offense.robot_id

	return send_val


def move_straight(TH_goal_info,offense,ball_info):
	send_val=SEND()

	TH_robot_info=calculate.Calc(TH_goal_info,offense.pose)
	TH_robot_degree=TH_robot_info.degree_calc()-math.degrees(offense.pose.theta)
	TH_robot_distance=TH_robot_info.distance_calc()
	TH_robot_degree=calculate.degree_improve(TH_robot_degree)

	robot_ball_info=calculate.Calc(offense.pose,ball_info.pose)
	robot_ball_degree=robot_ball_info.degree_calc()-math.degrees(offense.pose.theta)+180
	robot_ball_distance=robot_ball_info.distance_calc()
	robot_ball_degree=calculate.degree_improve(robot_ball_degree)

	ball_detect=False
	if robot_ball_degree<=3 and robot_ball_degree>=-3:
		ball_detect=True

	spinner=False
	if robot_ball_distance<0.12 and ball_detect==True:
		spinner=True

	if spinner==True and ball_detect==True:
		direction=TH_robot_degree
	else:
		direction=robot_ball_degree

	kick_pow_x=0
	if TH_robot_degree>=-5 and TH_robot_degree<=5:
		kick_pow_x=10.0

	send_val.stop=False
	send_val.direction=math.radians(direction)
	send_val.move_degree=math.radians(robot_ball_degree)
	send_val.spinner=True
	send_val.kickspeedx=kick_pow_x
	send_val.distance=robot_ball_distance

	if send_val.distance>=1:
		send_val.distance=1
	send_val.robot_id=attacker.robot_id

	return send_val

def pass_move(TH_goal_info,attacker,offense,ball_info,geometry,target,flag):
	send_val=SEND()

	TARGET_POSITION_X=3.5
	TARGET_POSITION_Y=-3.5

	AT_TH_info=calculate.Calc(attacker.pose,TH_goal_info)
	AT_TH_distance=AT_TH_info.distance_calc()
	AT_TH_degree=AT_TH_info.degree_calc()

	AT_OFF_info=calculate.Calc(attacker.pose,offense.pose)
	AT_OFF_distance=AT_OFF_info.distance_calc()
	AT_OFF_degree=AT_OFF_info.degree_calc()-math.degrees(offense.pose.theta)

	robot_ball_info=calculate.Calc(offense.pose,ball_info.pose)
	robot_ball_degree=robot_ball_info.degree_calc()-math.degrees(offense.pose.theta)+180
	robot_ball_degree=calculate.degree_improve(robot_ball_degree)
	robot_ball_distance=robot_ball_info.distance_calc()

	y=flag.slope*target.x+flag.intercept

	if flag.kick_flag==True:
		target_position=Pose2D(target.x, y, 0)
	else:
		target_position=Pose2D(target.x, target.y, 0)
	
	if flag.different_place==True:
		target_position=Pose2D(target.x, target.y, 0)

	target_position=position.line_limit(target_position,geometry)

	flag.arrive[flag.count_offense]=False
	if (target.x-0.1) <= offense.pose.x and (target.x+0.1) >= offense.pose.x:
		if (target.y-0.1) <= offense.pose.y and (target.y+0.1) >= offense.pose.y:
			flag.arrive[flag.count_offense]=True

	target_robot_info=calculate.Calc(target_position,offense.pose)
	target_robot_distance=target_robot_info.distance_calc()
	target_robot_degree=target_robot_info.degree_calc()-math.degrees(offense.pose.theta)
	target_robot_degree=calculate.degree_improve(target_robot_degree)

	TH_robot_info=calculate.Calc(TH_goal_info,offense.pose)
	TH_robot_degree=TH_robot_info.degree_calc()-math.degrees(offense.pose.theta)
	TH_robot_distance=TH_robot_info.distance_calc()

	ball_detect=False
	if robot_ball_degree<=10 and robot_ball_degree>=-10:
		ball_detect=True

	spinner=False
	if robot_ball_distance<0.15 and ball_detect==True:
		spinner=True

	if spinner==True and ball_detect==True:
		direction=TH_robot_degree
	else:
		direction=robot_ball_degree

	kick_pow_x=0
	if TH_robot_degree>=-5 and TH_robot_degree<=5:
		kick_pow_x=5.0

	if robot_ball_distance<0.15:
		flag.kick_flag=False

	send_val.stop=False
	send_val.direction=math.radians(direction)
	send_val.move_degree=math.radians(target_robot_degree)
	send_val.spinner=spinner
	send_val.kickspeedx=kick_pow_x
	send_val.distance=target_robot_distance*6
	if send_val.distance>=1:
		send_val.distance=1
	send_val.robot_id=offense.robot_id

	return send_val

def normal_position(attacker,offense,devide,ball_info,geometry,count):
	target_position=Pose2D()
	if len(devide.offense)==4:
		if count==1:
			target_position=Pose2D(0,0,0)
		elif count==2:
			target_position=Pose2D(4.5,3.5,0)
		elif count==3:
			target_position=Pose2D(4.5,-3.5,0)
		elif count==4:
			target_position=Pose2D(3.5,0,0)
	elif len(devide.offense)==3:
		if count==1:
			target_position=Pose2D(0,0,0)
		elif count==2:
			target_position=Pose2D(3.5,3.5,0)
		elif count==3:
			target_position=Pose2D(3.5,-3.5,0)
	elif len(devide.offense)==2:
		if count==1:
			target_position=Pose2D(0,0,0)
		elif count==2:
			target_position=Pose2D(3.5,3.5,0)
	elif len(devide.offense)==1:
		if count==1:
			target_position=Pose2D(2.5,3,0)

	target_robot_info=calculate.Calc(target_position,offense.pose)
	target_robot_degree=target_robot_info.degree_calc()-math.degrees(offense.pose.theta)+180
	target_robot_distance=target_robot_info.distance_calc()
	target_robot_degree=calculate.degree_improve(target_robot_degree)

	robot_ball_info=calculate.Calc(offense.pose,ball_info.pose)
	robot_ball_degree=robot_ball_info.degree_calc()-math.degrees(offense.pose.theta)+180
	robot_ball_distance=robot_ball_info.distance_calc()
	robot_ball_degree=calculate.degree_improve(robot_ball_degree)

	send_val=SEND()
	send_val.stop=False
	send_val.direction=math.radians(robot_ball_degree)
	send_val.move_degree=math.radians(target_robot_degree)
	send_val.spinner=False
	send_val.kickspeedx=0.0
	send_val.distance=target_robot_distance
	if send_val.distance>=1:
		send_val.distance=1
	send_val.robot_id=offense.robot_id

	return send_val