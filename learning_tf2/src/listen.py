#!/usr/bin/env python
import rospy
import tf
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

if __name__ == '__main__':
    # initialize node
    rospy.init_node('tf_listener', disable_signals = True)
    # print in console that the node is running
    rospy.loginfo('started listener node !')
    # create tf listener
    listener = tf.TransformListener()
    # set the node to run 1 time per second (1 hz)
    rate = rospy.Rate(10)
    # loop forever until roscore or this node is down
    frames = ['object_0', 'object_1', 'object_2']
   
    counter = 0

    while not rospy.is_shutdown():
	    for frame in frames:
		try:
		    # listen to transform
		    (pos,trans) = listener.lookupTransform('map','table '+ frame, rospy.Time())
		    # print the transform
		    rospy.loginfo('Moving to frame %s', frame)
		    


		    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		    client.wait_for_server()

		    goal = MoveBaseGoal()
		    goal.target_pose.header.frame_id = "map"
		    goal.target_pose.header.stamp = rospy.Time.now()
		    goal.target_pose.pose.position.x = pos[0]
		    goal.target_pose.pose.position.y = pos[1]
		    goal.target_pose.pose.orientation.w = 1.0
		    client.send_goal(goal)
		    wait = client.wait_for_result()
                    counter += 1
		    if not wait:
		       rospy.logerr("Action server not available!")
		       rospy.signal_shutdown("Action server not available!")
                    if counter == 3:
                        rospy.loginfo("Moving to initial location!")
                        goal.target_pose.pose.position.x = -0.712897
		        goal.target_pose.pose.position.y = 2.020490
		        goal.target_pose.pose.orientation.w = 1.0
		        client.send_goal(goal)
		        wait = client.wait_for_result()
                        rospy.loginfo("Execution Complete!")
                        reason = "Process Execution complete!"
                        rospy.signal_shutdown(reason) 
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		    continue
    		
		# sleep to control the node frequency
                rate.sleep()
   
