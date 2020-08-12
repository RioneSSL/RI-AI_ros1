#!/usr/bin/env python2
# coding: UTF-8

import rospy
import math
import signal
from geometry_msgs.msg import Pose2D
from RI_AI_msg.msg import RobotInfo,BALL_INFO,SEND,GEOMETRY,LINEINFO,ARCINFO,Referee,Ditection,Message,Flag,ROLE,Position,Attacker
import referee_translate
import Role
import calculate
import attacker
import goalie
import defense
import offense
import position
import time, threading
import homeposition
import kickoff


class Main(object):
	def __init__(self):

		self.our_robot_info = {'our':[],'their':[]}
		self.our_robot_info['our'].append(RobotInfo())
		self.ball_info_msg = []
		self.ball_info_msg.append(BALL_INFO())
		self.geometry_msg = GEOMETRY()
		self.send_msg=[]
		self.referee_info=Referee()
		self.sub_referee_info=rospy.Subscriber("referee_info",Referee,self.referee_callback,queue_size=1)
		self.sub_robot_our_info=rospy.Subscriber("vision_our_robot_info",Ditection,self.our_robot_callback,callback_args=0,queue_size=1)
		self.sub_ball_info=rospy.Subscriber("ball_info",BALL_INFO,self.ball_callback,queue_size=1)
		self.sub_geomerty_info=rospy.Subscriber("geometry_message",GEOMETRY,self.geometry_callback,queue_size=1)
		self.pub_robot_our_info=rospy.Publisher("vision_our_send",RobotInfo,queue_size=1)
		self.pub_send_info=rospy.Publisher("send_value",Message,queue_size=1)
		self.pub_send=[]
		self.robot_blue=[]
		self.ball_info=BALL_INFO()
		self.count=0
		self.flag=Flag()
		self.devide=ROLE()
		self.Position=[]
		self.temp=Pose2D()
		self.velocity=0
		self.scheduler_count=0
		self.Place=Position()
		self.rem_place=Pose2D()
		self.attacker=Attacker()
		t=threading.Thread(target=self.scheduler)
		t.start()
		self.t=threading.Timer(0.02,self.scheduler)
		self.set_positio=Pose2D()
		self.ref_command_info=referee_translate.translate()
	def referee_callback(self,msg):
		self.referee_info=msg

	def geometry_callback(self,msg):
		self.geometry_msg=msg

	def ball_callback(self,msg):
		self.ball_info_msg = msg
		self.ball_info.pose.x = self.ball_info_msg.pose.x
		self.ball_info.pose.y = self.ball_info_msg.pose.y

	def our_robot_callback(self,msg,robot_id):
		self.count=self.count+1
		if self.count==1:
			for ID in range(8):
				self.robot_blue.append(msg.blue_info[0])
		for robot in msg.blue_info:
			self.robot_blue[robot.robot_id]=robot

	def pub_send_all(self,message):
		#self.send_msg.append(self.pub_send_info)
		self.pub_send_info.publish(message)

	def main(self):
		while self.count==0:
			MASUO_SSL=1
		ID_MOUNT=8
		COUNT=0
		message=Message()
		message.send=[]
		TH_goal_info=Pose2D(6,0,0)
		OUR_goal_info=Pose2D(-6,0,0)
		devide = Role.role_decision(self.robot_blue,self.ball_info,TH_goal_info,OUR_goal_info,self.count,self.geometry_msg)

		if self.flag.kick_flag==False:
			self.Place=calculate.pass_position(self.robot_blue,devide,self.geometry_msg)
		
		ref_command=self.ref_command_info.main(self.referee_info,self.ball_info,self.flag)
		ref_command="NORMAL_START"
		if ref_command=="HALT":
			attacker_position=position.main(self.robot_blue[0],self.geometry_msg)
			print(attacker_position)
			message.send.append(attacker.halt())
		elif self.flag.PLAY==True or ref_command=="NORMAL_START":
			TH_AT_info=calculate.Calc(TH_goal_info,self.robot_blue[devide.attacker].pose)
			TH_AT_distance=TH_AT_info.distance_calc()
			message.send.append(goalie.main(OUR_goal_info,self.robot_blue[devide.goalie],self.ball_info,self.geometry_msg))
			attacker_position=position.main(self.robot_blue[devide.attacker],self.geometry_msg)
			if self.flag.kick_flag==True and not self.velocity==0:
				self.flag.different_place=False
				place=self.rem_place
				message.send.append(offense.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.robot_blue[devide.attacker],self.ball_info,self.geometry_msg,place,self.flag))	
			else:
				if TH_AT_distance>5:
					place=Pose2D(100,0,0)
					for i in range(8):
						if self.flag.arrive[i]==True:
							place=self.Place.pass_position[i].pose
					self.rem_place=place
					message.send.append(attacker.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.ball_info,self.flag,place))
				else:
					message.send.append(attacker.move_straight(TH_goal_info,self.robot_blue[devide.attacker],self.ball_info))
			
			self.flag.count_offense=-1
			for offense_id in devide.offense:		
				self.flag.count_offense=self.flag.count_offense+1
				self.flag.different_place=False
				place=self.Place.pass_position[self.flag.count_offense].pose
				#message.send.append(offense.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.robot_blue[offense_id],self.ball_info,self.geometry_msg,place,self.flag))
				message.send.append(offense.normal_position(self.robot_blue[devide.attacker],self.robot_blue[offense_id],devide,self.ball_info,self.geometry_msg,self.flag.count_offense))
		elif ref_command=="STOP":
			homeposition.stop_move(TH_goal_info,OUR_goal_info,self.robot_blue,devide,self.ball_info,self.geometry_msg,message)
		elif ref_command=="FORCE_START":
			send=attacker.halt(send)
		elif ref_command=="OUR_KICKOFF_START":
			kickoff.main(TH_goal_info,OUR_goal_info,self.robot_blue,devide,self.ball_info,self.geometry_msg,message)
		elif ref_command=="THEIR_KICKOFF_START":
			homeposition.main(TH_goal_info,OUR_goal_info,self.robot_blue,devide,self.ball_info,self.geometry_msg,message)
		elif ref_command=="OUR_PANALTY_PRE":
			send=attacker.halt(send)
		elif ref_command=="THEIR_PENALTY_PRE":
			send=attacker.halt(send)
		elif ref_command=="OUR_DIRECT":
			TH_AT_info=calculate.Calc(TH_goal_info,self.robot_blue[devide.attacker].pose)
			TH_AT_distance=TH_AT_info.distance_calc()
			message.send.append(goalie.main(OUR_goal_info,self.robot_blue[devide.goalie],self.ball_info,self.geometry_msg))
			attacker_position=position.main(self.robot_blue[devide.attacker],self.geometry_msg)
			if self.flag.kick_flag==True and not self.velocity==0:
				self.flag.different_place=False
				place=self.rem_place
				message.send.append(offense.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.robot_blue[devide.attacker],self.ball_info,self.geometry_msg,place,self.flag))	
			else:
				if TH_AT_distance>5:
					place=Pose2D(100,0,0)
					for i in range(8):
						if self.flag.arrive[i]==True:
							place=self.Place.pass_position[i].pose
					self.rem_place=place
					message.send.append(attacker.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.ball_info,self.flag,place))
				else:
					message.send.append(attacker.move_straight(TH_goal_info,self.robot_blue[devide.attacker],self.ball_info))
			
			self.flag.count_offense=-1
			for offense_id in devide.offense:		
				self.flag.count_offense=self.flag.count_offense+1
				self.flag.different_place=False
				place=self.Place.pass_position[self.flag.count_offense].pose
				message.send.append(offense.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.robot_blue[offense_id],self.ball_info,self.geometry_msg,place,self.flag))

		elif ref_command=="THEIR_DIRECT":
			send=attacker.halt(send)
		elif ref_command=="OUR_INDIRECT":
			TH_AT_info=calculate.Calc(TH_goal_info,self.robot_blue[devide.attacker].pose)
			TH_AT_distance=TH_AT_info.distance_calc()
			message.send.append(goalie.main(OUR_goal_info,self.robot_blue[devide.goalie],self.ball_info,self.geometry_msg))
			attacker_position=position.main(self.robot_blue[devide.attacker],self.geometry_msg)
			if self.flag.kick_flag==True and not self.velocity==0:
				self.flag.different_place=False
				place=self.rem_place
				message.send.append(offense.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.robot_blue[devide.attacker],self.ball_info,self.geometry_msg,place,self.flag))	
			else:
				if TH_AT_distance>5:
					place=Pose2D(100,0,0)
					for i in range(8):
						if self.flag.arrive[i]==True:
							place=self.Place.pass_position[i].pose
					self.rem_place=place
					message.send.append(attacker.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.ball_info,self.flag,place))
				else:
					message.send.append(attacker.move_straight(TH_goal_info,self.robot_blue[devide.attacker],self.ball_info))
			
			self.flag.count_offense=-1
			for offense_id in devide.offense:		
				self.flag.count_offense=self.flag.count_offense+1
				self.flag.different_place=False
				place=self.Place.pass_position[self.flag.count_offense].pose
				message.send.append(offense.pass_move(TH_goal_info,self.robot_blue[devide.attacker],self.robot_blue[offense_id],self.ball_info,self.geometry_msg,place,self.flag))

		elif ref_command=="THEIR_INDIRECT":
			send=attacker.halt(send)
		self.pub_send_all(message)

	def scheduler(self):
		self.t=threading.Timer(0.02,self.scheduler)
		self.t.start()
		self.velocity=self.ball_info.pose.x- self.temp.x
		y=self.ball_info.pose.y-self.temp.y
		self.temp.x=self.ball_info.pose.x
		self.temp.y=self.ball_info.pose.y
		if not self.velocity==0:
			self.flag.slope=y/self.velocity
			self.flag.intercept=self.ball_info.pose.y-self.flag.slope*self.ball_info.pose.x

	def stop(self):

		message=Message()
		message.send=[]
		#message.send.append(attacker.main(Pose2D(0,0,0),self.robot_blue[0],self.ball_info))
		for i in range(8):
			send_val=SEND()
			send_val.robot_id=i
			send_val.stop=True
			send_val.move_degree=-1
			message.send.append(send_val)
		#print(message)
		self.pub_send_all(message)

	def close(self):
		self.t.cancel()

if __name__=="__main__":
	rospy.init_node("main")
	r=rospy.Rate(60)
	proto=Main()
	rospy.on_shutdown(proto.stop)
	while not rospy.is_shutdown():
		proto.main()
		r.sleep()
	proto.close()
	