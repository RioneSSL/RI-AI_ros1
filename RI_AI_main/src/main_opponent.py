#!/usr/bin/env python2
# coding: UTF-8

import rospy
import math
from geometry_msgs.msg import Pose2D
from RI_AI_msg.msg import RobotInfo,BALL_INFO,SEND,GEOMETRY,LINEINFO,ARCINFO,Referee,Ditection,Message
import referee_translate
import Role
import calculate
import attacker
import goalie
import defense

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
		print(msg)
		if self.count==1:
			for ID in range(8):
				self.robot_blue.append(msg.yellow_info[0])
		for robot in msg.yellow_info:
			self.robot_blue[robot.robot_id]=robot

	def pub_send_all(self,message):
		#self.send_msg.append(self.pub_send_info)
		self.pub_send_info.publish(message)

	def main(self):
		while self.count==0:
			MASUO_SSL=1
		ID_MOUNT=8
		message=Message()
		sender=SEND()
		senderw=SEND()
		sendero=SEND()
		message.send=[]
		TH_goal_info=Pose2D(6,0,0)
		OUR_goal_info=Pose2D(-6,0,0)
		devide = Role.role_decision(self.robot_blue,self.ball_info,TH_goal_info,OUR_goal_info,self.count)
		ref_command=referee_translate.main(self,self.referee_info)
		ref_command="STOP"
		if ref_command=="HALT":
			send=attacker.halt(send)
		elif ref_command=="STOP":
			#message.send.append(goalie.main(OUR_goal_info,self.robot_blue[devide.goalie],self.ball_info,self.geometry_msg,senderw))
			#message.send.append(attacker.main(TH_goal_info,self.robot_blue[devide.attacker],self.ball_info,sender))
			#for defense_id in devide.defense:
			sendero=SEND()
				#message.send.append(defense.main(OUR_goal_info,self.robot_blue[defense_id],self.ball_info,self.geometry_msg,sendero))
		elif ref_command=="NORMAL_START":
			send=attacker.halt(send)
		elif ref_command=="FORCE_START":
			send=attacker.halt(send)
		elif ref_command=="OUR_KICKOFF_START":
			send=attacker.main(TH_goal_info,self.robot_blue[devide.attacker],self.ball_info,send)
		elif referee_command=="THEIR_KICKOFF_START":
			send=attacker.halt(send)
		elif ref_command=="OUR_PANALTY_PRE":
			send=attacker.halt(send)
		elif ref_command=="THEIR_PENALTY_PRE":
			send=attacker.halt(send)
		elif ref_command=="OUR_DIRECT":
			send=attacker.halt(send)
		elif ref_command=="THEIR_DIRECT":
			send=attacker.halt(send)
		elif ref_command=="OUR_INDIRECT":
			send=attacker.halt(send)
		elif ref_command=="THEIR_INDIRECT":
			send=attacker.halt(send)
		self.pub_send_all(message)

if __name__=="__main__":
	
	rospy.init_node("main")
	r=rospy.Rate(60)
	proto=Main()

	while not rospy.is_shutdown():
		proto.main()
		r.sleep()

	#message=SEND()
	#message.stop=True
	#proto.pub_send_all(message)
