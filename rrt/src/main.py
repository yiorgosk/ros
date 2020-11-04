#!/usr/bin/env python2
from map_manager import Map_manager
from planner import Planner
from controller import Controller
from operator import attrgetter
import rospy
import matplotlib.pyplot as plt
from geometry_msgs.msg import PoseStamped
import math

if __name__=='__main__':

	debug=True
	step_size=6

	rospy.init_node('rrt_demo1', anonymous=True)
	rate = rospy.Rate(10)
	map_location=rospy.get_param('/map_file','/home/lascm/catkin_ws/src/rrt/maps/point_map')
	rospy.loginfo("{}.png".format(map_location))

	manager=Map_manager()
	manager.map_manager(map_location+".png")
	planner=Planner(manager, step_size)
	control=Controller()
	control.controller(step_size)

	start_state, end_state = [], []
	start_point, end_point= [], []

	start_state.append(-2.0)
	start_state.append(0.5)

	end_state.append(0.5)
	end_state.append(2.0)
	end_state.append(0)

	final_yaw=end_state[2]

	end_point=manager.grid_coordinate(end_state)
	start_point=manager.grid_coordinate(start_state)

	if debug:
	    print("Start Point {}, {}\n".format(start_point[0], start_point[1]))
	    print("End Point {}, {}\n".format(end_point[0], end_point[1]))
	

	plan=PoseStamped()
	plan=planner.make_plan(start_point, end_point)
	
	rospy.loginfo("Plotting MAP with Global plan")
        for i in range(384):
            for j in range(384):
                if manager.get_state(i,j)>150:
                    x, y=[],[]
                    x.append((i*0.05)-10)
                    x.append((i*0.05)-10+0.01)
                    y.append((j*0.05)-10)
                    y.append((j*0.05)-10+0.01)
                    plt.plot(x,y)
        x,y=[],[]
        for i in range(len(plan)):
            x.append(plan[i].pose.position.x)
            y.append(plan[i].pose.position.y)
        plt.plot(x,y)
        plt.xlim(-10,10)
        plt.ylim(-10,10)
        plt.show()

    
        control.execute_plan(plan, final_yaw)
	rate.sleep()
	rospy.spin()

