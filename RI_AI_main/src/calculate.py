#!/usr/bin/env python2
# coding: UTF-8
import math
import time
from RI_AI_msg.msg import Position,PASS
from geometry_msgs.msg import Pose2D

class Calc(object):
	def __init__(self,object1,object2):
		self.difference_x=object1.x-object2.x
		self.difference_y=object1.y-object2.y
		self.degree=0
		self.a_constant=-0.002102256
		self.b_constant=1.647918685
		self.c_constant=-1.932145886

	def distance_calc(self):
		distance=math.sqrt((self.difference_x*self.difference_x)+(self.difference_y*self.difference_y))
	
		return distance

	def degree_calc(self):
		self.degree=math.degrees(math.atan2(self.difference_y,self.difference_x))
		
		if self.degree>180:
			self.degree=degree-360

		return self.degree

	def wrap_calc(self,goal_degree):
		flag=False
		degree=self.degree_calc()+180
		degree=degree_improve(degree-goal_degree)
		if degree<0:
			flag=True
			degree=math.fabs(degree)

		wrap_degree=self.a_constant*degree*degree+self.b_constant*degree+self.c_constant
		
		if flag==True:
			wrap_degree=(wrap_degree-360)*(-1)

		if wrap_degree>180:
			wrap_degree=wrap_degree-360

		return wrap_degree

def pass_position(robot,devide,geometry):
	POSITION=Position()
	POSITION_DISTANCE=2.0
	ratio=0
	if not geometry.field_width==0:
		ratio=80/(geometry.field_width/2)	
	left_degree=60-robot[devide.attacker].pose.y*ratio
	left_degree=-left_degree
	for i in range(4):
		pass_posi=PASS()
		X=(3.8)*math.cos(math.radians(left_degree+60*i))
		Y=(3.8)*math.sin(math.radians(left_degree+60*i))
		X=robot[devide.attacker].pose.x+X
		Y=robot[devide.attacker].pose.y-Y
		pass_posi.pose=Pose2D(X,Y,0)
		POSITION.pass_position.append(pass_posi)

	#print(devide)
	#print(POSITION.pass_position[0].pose.x)
	return POSITION

def velocity_calc():
	print(time.time())

def degree_improve(degree):
	if degree>360:
		degree=degree-360
	elif degree<-360:
		degree=degree+360
	elif degree<-180:
		degree=degree+360
	elif degree>180:
		degree=degree-360

	return degree

def kick_offense_posiiton_calc(offense,field_width):
	target_position=PASS()
	position=Position()
	offense_count=0
	for i in offense:
		if not i==-1:
			offense_count=offense_count+1
	separate=4
	if offense_count==4:
		separate=6
	val=field_width/separate
	if offense_count==1:
		target_position=Pose2D(-0.5,3.5,0)
		position.offense_position.append(target_position)
	elif offense_count==2:
		target_position=Pose2D(-0.5,3.5,0)
		position.offense_position.append(target_position)
		target_position=Pose2D(-0.5,-3.5,0)
		position.offense_position.append(target_position)
	elif offense_count==3:
		target_position=Pose2D(-0.5,3.5,0)
		position.offense_position.append(target_position)
		target_position=Pose2D(-0.5,-3.5,0)
		position.offense_position.append(target_position)
		target_position=Pose2D(-2,0,0)
		position.offense_position.append(target_position)
	elif offense_count==4:
		target_position=Pose2D(-0.5,3.5,0)
		position.offense_position.append(target_position)
		target_position=Pose2D(-0.5,-3.5,0)
		position.offense_position.append(target_position)
		target_position=Pose2D(-2,1.5,0)
		position.offense_position.append(target_position)
		target_position=Pose2D(-2,-1.5,0)
		position.offense_position.append(target_position)

	return position.offense_position

def offense_posiiton_calc(offense,field_width):
	target_position=[]
	offense_count=0
	for i in offense:
		if not i==-1:
			offense_count=offense_count+1
	separate=4
	if offense_count==4:
		separate=6
	val=field_width/separate
	if offense_count==1:
		target_position.append(0)
	elif offense_count==2:
		target_position.append(val)
		target_position.append(val*(-1))
	elif offense_count==3:
		target_position.append(0)
		target_position.append(val)
		target_position.append(-val)
	elif offense_count==4:
		target_position.append(val)
		target_position.append(-val)
		target_position.append(val*2)
		target_position.append(val*(-2))

	return target_position

def defense_position_calc(defense,field_width):
	target_position=[]
	defense_count=0
	for i in defense:
		if not i==-1:
			defense_count=defense_count+1
	if defense_count==1:
		target_position.append(0)
	if defense_count==2:
		target_position.append(0.2)
		target_position.append(-0.2)

	return target_position


