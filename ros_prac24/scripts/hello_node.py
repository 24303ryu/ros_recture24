#!/usr/bin/env python3
import rospy

rospy.init_node('hello_node')

r = rospy.Rate(1)
while not rospy.is_shutdown():
    rospy.loginfo("Hello World!")
    rospy.loginfo("num: %s",1)
    rospy.logwarn("num: %s",2)
    rospy.logerr("num: %s",3)
    rospy.logfatal("num: %s",4)

    r.sleep()

