#!/usr/bin/env python
import sys
from PyQt5.QtWidgets import QWidget, QApplication,QLabel,QFileDialog,QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QFont,QImage, QPixmap
from PyQt5.QtCore import Qt , QPoint
import rospy
import math
import copy
import rosparam
from std_msgs.msg import String
from RI_AI_msg.msg import BALL_INFO, RobotInfo, GEOMETRY ,LINEINFO
from geometry_msgs.msg import Pose2D

class App(QWidget):
    def __init__(self):
        super(App,self).__init__()
        self.title = "Masuo"
        self.geometry_msg=GEOMETRY()
        self.geometry_msg.field_length=1
        self.geometry_msg.field_width=1
        self.left = 0
        self.top = 0
        self.size=self.size()
        self.width = 640
        self.height = 480
        self.scale=0
        self.ui_height=600
        self.ui_width=440
        self.SETTING_X=0
        self.SETTING_Y=0
        self.field_lines=[]
        self.our_robot_info={"our":[],"their":[]}
        self.our_robot_info["our"].append(RobotInfo())
        self.ball_info=BALL_INFO()
        self.sub_ball_info=rospy.Subscriber("ball_info",BALL_INFO,self.callback_ball_info,queue_size=1)
        self.sub_robot_info=rospy.Subscriber("vision_our_robot_info",RobotInfo,self.callback_robot_info,queue_size=1)
        self.sub_robot_info=rospy.Subscriber("geometry_message",GEOMETRY,self.callback_geometry,queue_size=1)
        self.picture_draw()
        self.initUI()
        
    def callback_geometry(self,msg):
        self.geometry_msg=msg
        #print(msg.line_field.name)
        #for field_lines_info in msg.field_lines:
        #    geometry_line[field_lines_info]=[Pose2D(field_lines_info.p1_x,field_lines_info.p2_y)]
        self.update()

    def callback_robot_info(self,msg):
        self.our_robot_info["our"][0]=msg
        self.update()

    def picture_draw(self):
        label2=QLabel("supported by :",self)

        label=QLabel(self)
        pixmap = QPixmap('masuo1.png')
        label.setPixmap(pixmap)
        label.move(20,510)
        label2.move(2,488)

    def paintEvent(self,event):
        self.SETTING_X=self.ui_height/self.geometry_msg.field_length
        self.SETTING_Y=self.ui_width/self.geometry_msg.field_width
        ui=QPainter(self)
        ui.setBrush(QColor("teal"))
        ui.drawRect(self.left,self.top,self.width,self.height)
        ui.setPen(QColor(Qt.black))
        ui.setBrush(QColor(Qt.green))
        ui.drawRect(20,20,600,440)
        ui.setBrush(QColor(Qt.yellow))
        ui.drawPoint(320,240)
        ui.setBrush(QColor("orange"))
        center_ball=QPoint(self.ball_info.coordinate.x*self.SETTING_X+320,-(self.ball_info.coordinate.y*self.SETTING_Y)+240)
        center_robot=QPoint(self.our_robot_info["our"][0].pose.x*self.SETTING_X+320,-(self.our_robot_info["our"][0].pose.y*self.SETTING_Y)+240)
        ui.drawEllipse(center_ball,4,4)
        ui.setBrush(QColor("blue"))
        ui.drawEllipse(center_robot,6,6)
        self.field_setup(ui)
        self.drawLine(ui)

        

    def field_setup(self,ui):
        self.scale=1/self.width

    def drawLine(self,ui):
        ui.setBrush(QColor(Qt.yellow))
        ui.setPen(QColor(Qt.white))
        for field_lines_info in self.geometry_msg.line_field:
            ui.drawLine(field_lines_info.p1_x*self.SETTING_X+320,-field_lines_info.p1_y*self.SETTING_Y+240,field_lines_info.p2_x*self.SETTING_X+320,-field_lines_info.p2_y*self.SETTING_Y+240)

    def resizeEvent(self,event):
        t=0

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def callback_ball_info(self,msg):
        self.ball_info=msg
        self.update()
        

    def main(self):
        for i in range(100):
            ui.drawEllipse(300,300,14+i,14)
            print(i)
        

if __name__ == "__main__":
    rospy.init_node('Masuo')
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
        
    


