#!/usr/bin/env python3

import rospy
import random
from geometry_msgs.msg import Twist

cmd_vel = Twist()
cmd_vel.linear.x = 2.0
cmd_vel.angular.z = 0.8

def autonomous_controller():
    rospy.init_node('my_pub_test')
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
   
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish(cmd_vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        autonomous_controller()
    except rospy.ROSInterruptException:
        pass
