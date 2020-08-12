#!/usr/bin/env python2
# coding: UTF-8
import rospy
import multicast
import math
import referee_pb2
from consai2_msgs.msg import Referee
from geometry_msgs.msg import Point

class REFEREE(object):
	def __init__(self):
		self.HOST="224.5.23.1"
		self.PORT=10003
		self.sock=multicast.Multicast(self.HOST,self.PORT)
		self.pub_referee=rospy.Publisher("referee_info",Referee,queue_size=1)


	def recieve(self):
		BUF_LENGTH=2048
		buf=self.sock.recv(BUF_LENGTH)

		if buf:
			self.publish_referee(buf)

	def publish_referee(self,buf):
		packet_referee=referee_pb2.SSL_Referee()
		packet_referee.ParseFromString(buf)
		referee=Referee()
		referee.stage=packet_referee.stage
		if packet_referee.HasField("stage_time_left"):
			referee.stage_time_left=packet_referee.command_counter
		referee.command=packet_referee.command
		referee.command_counter=packet_referee.command_counter
		referee.command_timestamp=packet_referee.command_timestamp
		referee.yellow=packet_referee.yellow
		referee.blue=packet_referee.blue

		if packet_referee.HasField("designated_position"):
			referee.designated_position=Point(packet_referee.designated_position.x*0.001, packet_referee.designated_position.y*0.001,0)
		
		if packet_referee.HasField("blueTeamOnPositiveHalf"):
			referee.blue_team_on_positive_half=packet_referee.blueTeamOnPositiveHalf
		
		if packet_referee.HasField("gameEvent"):
			referee.game_event.game_event_type = packet_referee.gameEvent.gameEventType
			if packet_referee.gameEvent.HasField("originator"):
				referee.game_event.originator_team=packet_referee.gameEvent.originator.team
				if packet_referee.gameEvent.originator.HasFeild("botId"):
					referee.game_event.originator_bot_id=packet_referee.gameEvent.botId
			if packet_referee.gameEvent.HasField("message"):
				referee.game_event.message=packet_referee.gameEvent.message
		self.pub_referee.publish(referee)
		#print(referee)
		#print()

if __name__=="__main__":
	rospy.init_node("referee")
	r=rospy.Rate(60)
	receiver=REFEREE()
	while not rospy.is_shutdown():
		receiver.recieve()
		r.sleep()