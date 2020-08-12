#!/usr/bin/env python2
# coding: UTF-8

import rospy
import math
from geometry_msgs.msg import Pose2D
from RI_AI_msg.msg import RobotInfo,Role,Attacker,Goalie,PASS,Position

def role_decision(robot,ball_info,their_goal,our_goal,count,geometry):
	devide=Role()
	goalie=Goalie()
	attacker=Attacker()
	#our_goal_min(robot,our_goal,devide,goalie)
	devide.goalie=0
	find_ball_min(robot,ball_info,devide,attacker,geometry)	
	offense_decide(robot,devide,attacker,their_goal,geometry)
	defense_decide(robot,devide,goalie,our_goal)
	
	#print(devidebackground-size: cover)
	return devide


def find_ball_min(robot,ball_info,devide,attacker,geometry):
	POSITION_DISTANCE=2.0
	count=0
	attacker_pose_x=0
	attacker_pose_y=0
	distance_ball_min=0
	pass_position=[]
	devide.attacker=-1
	for robotq in robot:
		if not robotq.robot_id == devide.goalie:
			count=count+1
			distance_ball=math.sqrt((robotq.pose.x-ball_info.pose.x)*(robotq.pose.x-ball_info.pose.x)+(robotq.pose.y-ball_info.pose.y)*(robotq.pose.y-ball_info.pose.y))
			if distance_ball_min>distance_ball or count==1:
				distance_ball_min=distance_ball
				attacker.pose.x=robotq.pose.x
				attacker.pose.y=robotq.pose.y
				devide.attacker=robotq.robot_id
	#print(robot)
	

def our_goal_min(robot,our_goal,devide,goalie):
	count=0
	distance_our_goal_min=0
	goalie_pose_x=0
	goalie_pose_y=0
	for robot in robot:
		count=count+1
		distance_our_goal=math.sqrt((robot.pose.x-our_goal.x)*(robot.pose.x-our_goal.x)+(robot.pose.y-our_goal.y)*(robot.pose.y-our_goal.y))
		if distance_our_goal_min>distance_our_goal or count==1:
			distance_our_goal_min=distance_our_goal
			goalie.pose.x=robot.pose.x
			goalie.pose.y=robot.pose.y
			devide.goalie=robot.robot_id


def defense_decide(robotq,devide,defense,our_goal):
	defense_temp=0
	for ID in range(2):
		count=0
		distance_goalie_min=0
		defense_temp=-1
		for robot in robotq:
			if not robot.robot_id == devide.goalie and not robot.robot_id == devide.attacker and not robot.robot_id in devide.defense and not robot.robot_id in devide.offense:
				count=count+1
				distance_goalie=math.sqrt((robot.pose.x-our_goal.x)*(robot.pose.x-our_goal.x)+(robot.pose.y-our_goal.y)*(robot.pose.y-our_goal.y))
				if distance_goalie_min>distance_goalie or count==1:
					distance_goalie_min=distance_goalie
					defense_temp=robot.robot_id
		if not defense_temp==0 and not defense_temp==-1:
			devide.defense.insert(ID,defense_temp)
	devide.defense=sorted(devide.defense)

def offense_decide(robotq,devide,attacker,their_goal,geometry):
	offense_temp=0
	MAX_ID=8
	for ID in range(3):
		count=0
		distance_attacker_min=0
		offense_temp=-1
		for robot in robotq:
			if not robot.robot_id == devide.goalie and not robot.robot_id == devide.attacker and not robot.robot_id in devide.offense:
				count=count+1
				distance_attacker=math.sqrt((robot.pose.x-their_goal.x)*(robot.pose.x-their_goal.x)+(robot.pose.y-their_goal.y)*(robot.pose.y-their_goal.y))
				if distance_attacker_min > distance_attacker or count==1:
					distance_attacker_min = distance_attacker
					offense_temp=robot.robot_id
		if not offense_temp==0 and not offense_temp==-1:
			devide.offense.insert(ID,offense_temp)
	devide.offense=sorted(devide.offense)
	#for offense in devide.offense:
	#	distance_position


					



