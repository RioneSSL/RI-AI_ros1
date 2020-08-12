#!/usr/bin/env python2
# coding: UTF-8

import rospy 
import math
import socket
import grSim_Packet_pb2
from RI_AI_msg.msg import RobotInfo,DitectMasuo,BALL_INFO,SEND,Message

class Sender(object):
	def __init__(self):
		self.host='127.0.0.1'
		self.port=20011
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sub_robot_info=rospy.Subscriber("vision_our_send",RobotInfo,self.recieve_callback,callback_args=0,queue_size=1)
		self.sub_ball_info=rospy.Subscriber("ball_info",BALL_INFO,self.ball_callback,queue_size=1)
		self.sub_recieve_info=rospy.Subscriber("send_value",Message,self.send_value,queue_size=1)
		self.our_robot_info={"our":[],"their":[]}
		self.our_robot_info['our'].append(RobotInfo())
		self.ball_info=[]
		self.ball_info.append(BALL_INFO())
		self.recieve_info=[]
		self.recieve_info.append(SEND())
		self.move_degree=0

	def recieve_callback(self,msg):
		self.recieve_info=msg
		self.move_degree=self.recieve_info.degree
		#print(self.move_degree)

	def ball_callback(self,msg):
		self.ball_info=msg
		#print(self.ball_info)

	def robot_callback(self,msg):
		self.our_robot_info["our"][0]=msg

		#	print(self.our_robot_info)
		
	def send_value(self,msg):
		for msg in msg.send:
			self.recieve_info=msg
			self.move_deg=self.recieve_info.move_degree
			packet=grSim_Packet_pb2.grSim_Packet()
			packet.commands.timestamp=0
			packet.commands.isteamyellow=False
			packet_command=packet.commands.robot_commands.add()
			packet_command.id=self.recieve_info.robot_id
			packet_command.veltangent=math.cos(self.recieve_info.move_degree)*1.6*self.recieve_info.distance
			packet_command.velnormal=math.sin(self.recieve_info.move_degree)*1.6*self.recieve_info.distance
			packet_command.velangular=self.recieve_info.direction*4
			packet_command.kickspeedx=self.recieve_info.kickspeedx
			packet_command.kickspeedz=0
			packet_command.spinner=self.recieve_info.spinner
			packet_command.wheelsspeed=False
			#print(self.recieve_info.stop)
			if self.recieve_info.stop==True:
				#print(self.recieve_info.stop)
				packet_command.veltangent=0
				packet_command.velnormal=0
			message=packet.SerializeToString()
			self.sock.sendto(message,(self.host,self.port))

if __name__=="__main__":
	rospy.init_node("sender")
	send=Sender()
	rospy.spin()

