#!/usr/bin/env python2
# coding: UTF-8

import math
import rospy
import serial
from geometry_msgs.msg import Pose2D
from RI_AI_msg.msg import SEND,Message

class Sender(object):
	def __init__(self):
		self.DEVICE="/dev/ttyUSB0"
		self.BAUDRATE=57600
		self.MAX_VEL_NORM=4.0
		self.MAX_VEL_ANGULER=2.0*math.pi
		self.serial=serial.Serial(self.DEVICE,self.BAUDRATE)
		self.sub_commands=rospy.Subscriber("send_value",Message,self.send,queue_size=1)

	def send(self,msg):
		for message in msg.send:
			packet = bytearray()

			packet.append(0xFF)
			packet.append(0xC3)

			packet.append(message.robot_id)
			packet.append(message.stop)
			if message.direction < 0:
				message.direction += 2.0 * math.pi
			message.direction=math.degrees(message.direction)+0
			packet.append(int(message.direction/2.0))
			
			if message.move_degree<0:
				message.move_degree+=2.0*math.pi
			message.move_degree=math.degrees(message.move_degree)+0
			packet.append(int(message.move_degree/2.0))
			#packet.append(message.distance)
			packet.append(message.spinner)
			packet.append(int(message.kickspeedx))

			self.serial.write(packet)

			command_packet = 0
			power_packet = 0

	def close_serial(self):
		self.serial.close()

def main():
	rospy.init_node("real_sender")
	sender=Sender()

	rospy.on_shutdown(sender.close_serial)

	rospy.spin()

if __name__=="__main__":
	try:
		main()
	except rospy.ROSInitException:
		pass
