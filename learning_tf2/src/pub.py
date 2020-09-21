#!/usr/bin/env python  
import roslib


import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('fixed_tf_broadcaster')
    initial_pose = tf.TransformBroadcaster()
    table_1 = tf.TransformBroadcaster()
    table_2 = tf.TransformBroadcaster()
    table_3 = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        
        table_1.sendTransform((-2.61644761292, 2.61644761292, 0.0),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "table_1",
                         "map")
	table_2.sendTransform((4.983163, 2.794993, 0.0),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "table_2",
                         "map")
	table_3.sendTransform((5.5, -2.671566, 0.0),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "table_3",
                         "map")
        initial_pose.sendTransform((-3.000002, 1.000009, 0.0),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "initial_pose",
                         "map")
        rate.sleep()
