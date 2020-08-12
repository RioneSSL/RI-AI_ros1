import math
import rospy
import calculate
from geometry_msgs.msg import Pose2D
from RI_AI_msg.msg import SEND

def main(TH_goal_info,attacker,ball_info):
	send_val=SEND()

	TH_goal_robot=calculate.Calc(TH_goal_info,attacker.pose)
	TH_goal_robot_degree=TH_goal_robot.degree_calc()-attacker.pose.theta*180/3.14

	robot_ball_info=calculate.Calc(attacker.pose,ball_info.pose)
	robot_ball_degree=robot_ball_info.degree_calc()-attacker.pose.theta*180/3.14
	wrap_degree=robot_ball_info.wrap_calc(math.degrees(attacker.pose.theta))
	robot_ball_distance=robot_ball_info.distance_calc()	

	calculate.degree_improve(wrap_degree)
	calculate.degree_improve(robot_ball_degree)

	ball_detect=False
	if robot_ball_degree<=10 and robot_ball_degree>=-10:
		ball_detect=True
	
	spinner=False
	if robot_ball_distance<0.4 and ball_detect==True:
		spinner=True

	kick_pow_x=0
	if TH_goal_robot_degree>=-10 and TH_goal_robot_degree<=10:
		kick_pow_x=6.0
		
	send_val.direction=math.radians(TH_goal_robot_degree)
	send_val.move_degree=math.radians(wrap_degree)
	send_val.spinner=spinner
	send_val.distance=0.85
	send_val.kickspeedx=kick_pow_x
	send_val.robot_id=attacker.robot_id
	send_val.stop=True
	return send_val


def stop_posi(TH_goal_info,attacker,ball_info,DISTANCE):
	send_val=SEND()

	DISTANCE_SPACE=Pose2D(math.cos(attacker.pose.theta)*DISTANCE,math.sin(attacker.pose.theta)*DISTANCE,0)

	target_posi=Pose2D(ball_info.pose.x - DISTANCE_SPACE.x, ball_info.pose.y - DISTANCE_SPACE.y,0)
	TH_goal_robot=calculate.Calc(TH_goal_info,attacker.pose)
	TH_goal_robot_degree=TH_goal_robot.degree_calc()-attacker.pose.theta*180/3.14
	target_robot=calculate.Calc(target_posi,attacker.pose)
	target_robot_distance=target_robot.distance_calc()
	robot_ball_info=calculate.Calc(attacker.pose,target_posi)
	robot_ball_degree=robot_ball_info.degree_calc()-attacker.pose.theta*180/3.14
	wrap_degree=robot_ball_info.wrap_calc(math.degrees(attacker.pose.theta))
	robot_ball_distance=robot_ball_info.distance_calc()
	
	if target_robot_distance>=1:
		target_robot_distance=1

	wrap_degree = calculate.degree_improve(wrap_degree)

	robot_ball_degree = calculate.degree_improve(robot_ball_degree)

	ball_detect=False
	if robot_ball_degree<=10 and robot_ball_degree>=-10:
		ball_detect=True

	spinner=False
	if robot_ball_distance<0.4 and ball_detect==True:
		spinner=True

	kick_pow_x=0
	if TH_goal_robot_degree>=-10 and TH_goal_robot_degree<=10:
		kick_pow_x=0.0
	
	send_val.stop=False
	send_val.direction=math.radians(TH_goal_robot_degree)
	send_val.move_degree=math.radians(wrap_degree)
	send_val.spinner=True
	send_val.kickspeedx=kick_pow_x
	send_val.distance=target_robot_distance
	send_val.robot_id=attacker.robot_id

	return send_val

def move_straight(TH_goal_info,attacker,ball_info):
	send_val=SEND()

	TH_robot_info=calculate.Calc(TH_goal_info,attacker.pose)
	TH_robot_degree=TH_robot_info.degree_calc()-math.degrees(attacker.pose.theta)
	TH_robot_distance=TH_robot_info.distance_calc()
	TH_robot_degree=calculate.degree_improve(TH_robot_degree)

	robot_ball_info=calculate.Calc(attacker.pose,ball_info.pose)
	robot_ball_degree=robot_ball_info.degree_calc()-math.degrees(attacker.pose.theta)+180
	robot_ball_distance=robot_ball_info.distance_calc()
	robot_ball_degree=calculate.degree_improve(robot_ball_degree)

	ball_detect=False
	if robot_ball_degree<=10 and robot_ball_degree>=-10:
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
		kick_pow_x=8.0

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

def pass_move(TH_goal_info,attacker,ball_info,flag,target_position):
	send_val=SEND()

	TARGET_POSITION_X=3.5
	TARGET_POSITION_Y=-3.5
	TH_robot_info=calculate.Calc(TH_goal_info,attacker.pose)
	TH_robot_degree=TH_robot_info.degree_calc()-math.degrees(attacker.pose.theta)
	TH_robot_distance=TH_robot_info.distance_calc()
	TH_robot_degree=calculate.degree_improve(TH_robot_degree)

	robot_ball_info=calculate.Calc(attacker.pose,ball_info.pose)
	robot_ball_degree=robot_ball_info.degree_calc()-math.degrees(attacker.pose.theta)+180
	robot_ball_degree=calculate.degree_improve(robot_ball_degree)
	robot_ball_distance=robot_ball_info.distance_calc()

	#target_position=Pose2D(TARGET_POSITION_X, TARGET_POSITION_Y,0)
	target_robot_info=calculate.Calc(target_position,attacker.pose)
	target_robot_degree=target_robot_info.degree_calc()-math.degrees(attacker.pose.theta)
	target_robot_degree=calculate.degree_improve(target_robot_degree)
	target_robot_distance=target_robot_info.distance_calc()
	
	#print(target_robot_degree)
	ball_detect=False
	if robot_ball_degree<=5 and robot_ball_degree>=-5:
		ball_detect=True

	spinner=False
	if ball_detect==True and robot_ball_distance<0.12:
		spinner=True

	kick_pow_x=0
	direction=robot_ball_degree
	if spinner==True and ball_detect==True:
		direction=target_robot_degree
		if target_robot_degree>=-5 and target_robot_degree<=5 and not target_position.x == 100:
			kick_pow_x=5
			flag.flag_temp=True

	if flag.flag_temp==True:
		if robot_ball_distance>0.2:
			flag.flag_temp=False
			flag.kick_flag=True
			flag.robot_id_rem=attacker.robot_id

	if not attacker.robot_id == flag.robot_id_rem and  robot_ball_distance<0.3:
		flag.kick_flag=False

	send_val.stop=False
	send_val.direction=math.radians(direction)
	send_val.move_degree=math.radians(robot_ball_degree)
	send_val.spinner=spinner
	send_val.kickspeedx=kick_pow_x
	send_val.distance=robot_ball_distance
	send_val.robot_id=attacker.robot_id

	if send_val.distance>=1:
		send_val.distance=1

	return send_val


def halt():
	send_val=SEND()

	send_val.stop=True
	send_val.direction=0
	send_val.move_degree=-1
	send_val.spinner=False
	send_val.kickspeedx=0

	return send_val

