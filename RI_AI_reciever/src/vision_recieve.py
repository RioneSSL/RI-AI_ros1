#!/usr/bin/env python2
# coding: UTF-8
import rospy
import math
import multicast
import messages_robocup_ssl_wrapper_pb2 as ssl_wrapper
from RI_AI_msg.msg import RobotInfo,DitectMasuo,BALL_INFO,GEOMETRY,ARCINFO,LINEINFO,Ditection

class Receiver(object):
	def __init__(self):
		self.HOST="224.5.23.2"
		self.PORT=10020
		self.SIDE="left"
		self.SETTING=0.001
		self.sock=multicast.Multicast(self.HOST,self.PORT)
		self.pose_x=0
		self.pub_our_robot_info=rospy.Publisher("vision_our_robot_info",Ditection,queue_size=1)
		self.pub_ball_info=rospy.Publisher("ball_info",BALL_INFO,queue_size=1)
		self.pub_send_geometry=rospy.Publisher("geometry_message",GEOMETRY,queue_size=1)
		self.pub_send=[]
		self.pub_send2=[]

	def receive(self):
		BUF_LENGTH=2048
		buf=""
		while buf is not False:
			buf=self.sock.recv(BUF_LENGTH)
			if buf:
				packet = ssl_wrapper.SSL_WrapperPacket()
				packet.ParseFromString(buf)
				if packet.HasField("detection"):
					detect_value_t_capture=packet.detection.t_capture
					ball_info=BALL_INFO()
					detect_robot=Ditection()

					for robot in packet.detection.robots_blue:
						robot_info=DitectMasuo()
						robot_info.robot_id=robot.robot_id
						robot_info.pose.x=robot.x*self.SETTING
						robot_info.pose.y=robot.y*self.SETTING
						robot_info.pose.theta=robot.orientation
						detect_robot.blue_info.append(robot_info)

					#if detect_robot.blue_info:
					#	self.pub_our_robot_info.publish(detect_robot)

					#for robot in packet.detection.robots_yellow:
					#	robot_info=DitectMasuo()
					#	robot_info.robot_id=robot.robot_id
					#	robot_info.pose.x=robot.x*self.SETTING
					#	robot_info.pose.y=robot.y*self.SETTING
					#	robot_info.pose.theta=robot.orientation
					#	detect_robot.yellow_info.append(robot_info)

					if detect_robot.yellow_info or detect_robot.blue_info:
						self.pub_our_robot_info.publish(detect_robot)

					for ball in packet.detection.balls:
						ball_info.pose.x=ball.x*self.SETTING
						ball_info.pose.y=ball.y*self.SETTING
						self.pub_send2.append(self.pub_ball_info)
						self.pub_send2[0].publish(ball_info)

				if packet.HasField("geometry"):
					geometry=GEOMETRY()
					geometry.field_length=packet.geometry.field.field_length*self.SETTING
					geometry.field_width=packet.geometry.field.field_width*self.SETTING
					geometry.goal_width=packet.geometry.field.goal_width*self.SETTING
					geometry.goal_depth=packet.geometry.field.goal_depth*self.SETTING
					geometry.boundary_width=packet.geometry.field.boundary_width*self.SETTING

					
					for line in packet.geometry.field.field_lines:
						LINE=LINEINFO()
						LINE.name=line.name
						LINE.p1_x=line.p1.x*self.SETTING
						LINE.p1_y=line.p1.y*self.SETTING
						LINE.p2_x=line.p2.x*self.SETTING
						LINE.p2_y=line.p2.y*self.SETTING
						LINE.thickness=line.thickness
						geometry.line_field.append(LINE)

					for arc in packet.geometry.field.field_arcs:
						ARC=ARCINFO()
						ARC.name=arc.name
						ARC.center_x=arc.center.x*self.SETTING
						ARC.center_y=arc.center.y*self.SETTING
						ARC.radius=arc.radius*self.SETTING
						ARC.a1=arc.a1
						ARC.a2=arc.a2
						ARC.thickness=arc.thickness*self.SETTING
						geometry.arc_field.append(ARC)
					self.pub_send_geometry.publish(geometry)
					


if __name__ == '__main__':
	rospy.init_node("receive")
	r=rospy.Rate(60)
	rec=Receiver()
	while not rospy.is_shutdown():
		rec.receive()
		r.sleep()
