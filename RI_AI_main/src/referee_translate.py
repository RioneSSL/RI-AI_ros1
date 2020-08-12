import rospy
import math
import calculate
from geometry_msgs.msg import Pose2D

class translate(object):
	def __init__(self):
		self.set_position=0

	def main(self,ref_info,ball_info,flag):
		ref_command=""

		if ref_info.command==0:
			ref_command="HALT"
		elif ref_info.command==1:
			ref_command="STOP"
		elif ref_info.command==2:
			ref_command="NORMAL_START"
		elif ref_info.command==3:
			ref_command="FORCE_START"
		elif ref_info.command==4:
			ref_command="OUR_KICKOFF_START"
		elif ref_info.command==5:
			ref_command="THEIR_KICKOFF_START"
		elif ref_info.command==6:
			ref_command="OUR_PENALTY_PRE"
		elif ref_info.command==7:
			ref_command="THEIR_PENALTY_PRE"
		elif ref_info.command==8:
			ref_command="OUR_DIRECT"
		elif ref_info.command==9:
			ref_command="THEIR_DIRECT"
		elif ref_info.command==10:
			ref_command="OUR_INDIRECT"
		elif ref_info.command==11:
			ref_command="THEIR_INDIRECT"
		elif ref_info.command==12:
			ref_command="KICKOFF_START"

		flag.PLAY=False
		ball_pose=Pose2D()
		if ref_command == "OUR_PENALTY_PRE" \
			or ref_command == "OUR_DIRECT" or ref_command == "OUR_INDIRECT" or ref_command == "THEIR_KICKOFF_START" \
			or ref_command == "THEIR_PENALTY_PRE" or ref_command == "THEIR_DIRECT" or ref_command == "THEIR_INDIRECT":
			flag.count_position=flag.count_position+1
			if flag.count_position==1:
				self.set_position_x=ball_info.pose.x
				self.set_position_y=ball_info.pose.y
			distance_info=calculate.Calc(Pose2D(self.set_position_x,self.set_position_y,0),ball_info.pose)
			distance=distance_info.distance_calc()
		
		
			if distance>=0.1: 
				flag.PLAY=True
		else:
			flag.count_position=0
		#print(flag.PLAY)

		return ref_command

def set_position(ref_command,ball_info,flag):
	flag.PLAY=False
	if ref_command == "OUR_KICKOFF_START" or ref_command == "OUR_PENALTY_PRE" \
		or ref_command == "OUR_DIRECT" or ref_command == "OUR_INDIRECT" or ref_command == "THEIR_KICKOFF_START" \
		or ref_command == "THEIR_PENALTY_PRE" or ref_command == "THEIR_DIRECT" or ref_command == "THEIR_INDIRECT":
		flag.count_position=flag.count_position+1
		if flag.count_position==1:
			set_position=ball_info.pose
		distance_info=calculate.Calc(set_position,ball_info.pose)
		distance=distance_info.distance_calc()
		if distance>=0.1:
			flag.PLAY=True
	else:
		flag.count_position=0

	return set_position


if __name__=="__main__":
	main()

