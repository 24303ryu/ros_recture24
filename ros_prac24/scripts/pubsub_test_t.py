#!/usr/bin/env python3
import rospy
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

cmd_vel = Twist()

pose = Pose()
pose2 = Pose()

def update_pose(data):
    global pose
    pose.x = data.x
    pose.y = data.y
    pose.theta = data.theta

def update_pose2(data2):
    global pose2
    pose2.x = data2.x
    pose2.y = data2.y
    pose2.theta = data2.theta
def update_cmd_vel():
    global cmd_vel
    global vecx,vecy
    dx=pose.x-pose2.x
    dy=pose.y-pose2.y
    
    if(dx>0):
        vecx=1
    else:
        vecx=-1
    if(dy>0):
        vecy=1
    else:
        vecy=-1
    if(dx==0 or dy==0):
        a=1
    else:
        sita=math.atan(dy/dx)
        
        dxy=math.sqrt(dx*dx+dy*dy)
        cmd_vel.linear.x =math.cos(sita)
        cmd_vel.linear.y = math.sin(sita)
        print(sita)
        cmd_vel.angular.z=sita-pose2.theta
        
def autonomous_controller():
    rospy.init_node('autonomous_controller')
    pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    sub2 = rospy.Subscriber('/turtle2/pose', Pose, update_pose2)
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
