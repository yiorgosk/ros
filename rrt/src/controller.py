#!/usr/bin/env python
import rospy
import ros
from geometry_msgs.msg import PoseStamped
from math import atan, sqrt
from tf.transformations import quaternion_from_euler
from move_base_msgs.msg import MoveBaseActionFeedback


class Controller:
    def __init__(self):
        self.current_x=0
        self.current_y=0
        self.distance_threshold=0
	self.pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
	self.rate = rospy.Rate(10.0)

    def callback(self, msg):
        self.current_x=msg.feedback.base_position.pose.position.x
        self.current_y=msg.feedback.base_position.pose.position.y

    def controller(self, step_size):
        
        sub = rospy.Subscriber('/move_base/feedback', MoveBaseActionFeedback, self.callback)
        self.distance_threshhold = (step_size * 0.05) / 1.2

    def move_to_goal(self, point):
        print(point.pose.position.x, point.pose.position.y)
        point.header.frame_id = "map"
        point.header.stamp = rospy.Time.now()
	self.pub.publish(point)
	
    def execute_plan(self, plan, final_yaw):
        
        rospy.loginfo("Executing the plan")
	
        for i in range(len(plan)):
            x1, y1= 0,0
            x2,y2=0,0
            slope, rad=0,0

            if i==0:
                rad=final_yaw
            else:
                x1=plan[i].pose.position.x
                y1=plan[i].pose.position.y
                x2=plan[i].pose.position.x
                y2=plan[i].pose.position.y

                if x2==x1:
                    rad=y2>y1 and 1.5708 or -1.5708
                else:
                    slope=(y2-y1)/(x2-x1)
                    rad=atan(slope)
            quat=quaternion_from_euler(0,0,rad)
	    plan[i].pose.orientation.x=quat[0]
            plan[i].pose.orientation.y=quat[1]
            plan[i].pose.orientation.z=quat[2]
            plan[i].pose.orientation.w=quat[3]
            self.move_to_goal(plan[i])

            distance=0
            while self.distance_threshold<distance:
                distance=sqrt(pow(x1-self.current_x, 2)+pow(y1-self.current_y, 2))
                self.rate.sleep()
        return True
