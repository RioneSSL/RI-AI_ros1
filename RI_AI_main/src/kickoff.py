import math
import rospy
import attacker
import calculate
from RI_AI_msg.msg import SEND
from geometry_msgs.msg import Pose2D

def main(TH_goal_info,OUR_goal_info,robot_info,devide,ball_info,geometry,message):
	message.send.append(attacker.stop_posi(TH_goal_info,robot_info[devide.attacker],ball_info,0.12))

	target_position=Pose2D(-geometry.field_length/2,0,0)
	goalie_target_info=calculate.Calc(robot_info[devide.goalie].pose,target_position)
	goalie_target_degree=goalie_target_info.degree_calc() -  math.degrees(robot_info[devide.goalie].pose.theta) +180
	goalie_target_distance=goalie_target_info.distance_calc()
	goalie_target_degree=calculate.degree_improve(goalie_target_degree)
	if goalie_target_distance>=1:
		goalie_target_distance=1

	send_val=SEND()
	send_val.robot_id=robot_info[devide.goalie].robot_id
	send_val.distance=goalie_target_distance
	send_val.move_degree=math.radians(goalie_target_degree)
	send_val.direction=-robot_info[devide.goalie].pose.theta
	send_val.stop=False
	message.send.append(send_val)

	count=-1
	for offense_id in devide.offense:
		count=count+1
		target_position=calculate.kick_offense_posiiton_calc(devide.offense,geometry.field_width)
	
		offense_target_info=calculate.Calc(robot_info[offense_id].pose,target_position[count])
		offense_target_distance=offense_target_info.distance_calc()
		offense_target_degree=offense_target_info.degree_calc() -  math.degrees(robot_info[offense_id].pose.theta) +180
		offense_target_degree=calculate.degree_improve(offense_target_degree)
		if offense_target_distance>=1:
			offense_target_distance=1
		send_val=SEND()
		send_val.robot_id=robot_info[offense_id].robot_id
		send_val.distance=offense_target_distance
		send_val.move_degree=math.radians(offense_target_degree)
		send_val.stop=False
		send_val.direction=-robot_info[offense_id].pose.theta
		send_val.spinner=True
		send_val.kickspeedx=0.0

		message.send.append(send_val)

	count=-1
	for defense_id in devide.defense:
		count=count+1
		num=calculate.defense_position_calc(devide.defense,geometry.field_width)
		if len(num)>count:
			target_position=Pose2D(-4.5,num[count],0)
		defense_target_info=calculate.Calc(robot_info[defense_id].pose,target_position)
		defense_target_distance=defense_target_info.distance_calc()
		defense_target_degree=defense_target_info.degree_calc() - math.degrees(robot_info[defense_id].pose.theta) +180
		defense_target_degree=calculate.degree_improve(defense_target_degree)
		if defense_target_distance>=1:
			defense_target_distance=1
		send_val=SEND()
		send_val.robot_id=robot_info[defense_id].robot_id
		send_val.distance=defense_target_distance
		send_val.move_degree=math.radians(defense_target_degree)
		send_val.direction=-robot_info[defense_id].pose.theta
		send_val.stop=False
		send_val.spinner=True
		send_val.kickspeedx=0.0

		message.send.append(send_val)

