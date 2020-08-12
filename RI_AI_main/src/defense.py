import rospy
import math
import calculate
from geometry_msgs.msg import Pose2D
from RI_AI_msg.msg import SEND,Flag

def main(our_goal_info,defense,ball_info,geometry):
	send_val=SEND()

	penalty_length=0
	target_position=Pose2D()
	for line_field in geometry.line_field:
		if line_field.name=="LeftPenaltyStretch":
			penalty_length=line_field.p2_x
			target_position=Pose2D(penalty_length,ball_info.pose.y,0)
			if defense.pose.y>=math.fabs(line_field.p1_y):
				target_position.y=math.fabs(line_field.p1_y)
			elif defense.pose.y<=-math.fabs(line_field.p1_y):
				target_position.y=-math.fabs(line_field.p1_y)
			
	robot_target_info=calculate.Calc(target_position,defense.pose)
	robot_target_degree=robot_target_info.degree_calc() - math.degrees(defense.pose.theta) 

	robot_ball_info=calculate.Calc(defense.pose,ball_info.pose)
	robot_ball_degree=robot_ball_info.degree_calc() - math.degrees(defense.pose.theta) +180
	
	robot_target_degree=calculate.degree_improve(robot_target_degree)
	robot_ball_degree=calculate.degree_improve(robot_ball_degree)
	#print(penalty_length)
	send_val.stop=False
	send_val.direction=-defense.pose.theta
	send_val.move_degree=math.radians(robot_target_degree)
	send_val.spinner=True
	send_val.kickspeedx=0.0
	send_val.distance=math.fabs(math.radians(robot_ball_degree))
	send_val.robot_id=defense.robot_id

	return send_val
