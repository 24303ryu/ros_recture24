#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

cmd_vel = Twist()
cmd_vel.linear.x = 2.0
cmd_vel.angular.z = 0.0

pose = Pose()
nowRotating = False

def update_pose(data):
    global pose
    pose.x = data.x
    pose.y = data.y
    pose.theta = data.theta
def update_cmd_vel():
    global cmd_vel
    global nowRotating
    if (pose.x <1) and not nowRotating:
        cmd_vel.linear.x = 0.0
        cmd_vel.angular.z = 1.0
        if(pose.theta>0):
            nowRotating = True
    elif(pose.x > 9.8) and not nowRotating:
        cmd_vel.linear.x = 0.0
        cmd_vel.angular.z = 1.0
        if(pose.theta<0):
            nowRotating = True
    else:
        cmd_vel.linear.x = 2.0
        cmd_vel.angular.z = 0.0
        nowRotating = False
def autonomous_controller():
    rospy.init_node('autonomous_controller')
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/turtle1/pose', Pose, update_pose)


    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        update_cmd_vel()
        pub.publish(cmd_vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        autonomous_controller()
    except rospy.ROSInterruptException:
        pass
