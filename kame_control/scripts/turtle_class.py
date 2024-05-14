#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster
from tf.transformations import euler_from_quaternion
import math

class Pose:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
class Turtle1:
    def __init__(self):
        self.pos = Pose()
        self.vel = Twist()
        self.nh = rospy.init_node('my_Turtle1')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub_odom = rospy.Subscriber('/odom', Odometry, self.callback)
        self.vel.linear.x = self.vel.linear.y = self.vel.linear.z = 0.0
        self.vel.angular.z = self.vel.angular.y = self.vel.angular.x = 0.0

    def set_speed(self, x, theta):
        self.vel.linear.x = x
        self.vel.angular.z = theta
        self.pub.publish(self.vel)
    def callback(self, msg):
        self.pos.x = msg.pose.pose.position.x
        self.pos.y = msg.pose.pose.position.y
        roll, pitch, yaw = euler_from_quaternion([
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w
        ])
        self.pos.theta = yaw
        rospy.loginfo("/odom Pos (x:%f, y:%f, z:%f)", msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z)
        rospy.loginfo("/odom Pose (roll:%f, pitch:%f, yaw:%f) ", roll, pitch, yaw)
    def move_turtle1(self, x, theta, sec):
        tim = 0
        rate = rospy.Rate(10)
        while tim<sec*10:
            self.set_speed(x, theta)
            tim = tim + 1
            rate.sleep()
        self.set_speed(0.0, 0.0)
    def move_straight(self,x,length):
        init_x=self.pos.x
        init_y=self.pos.y
        d=0
        rate=rospy.Rate(50)
        while d<length:
            d=math.sqrt((self.pos.x-init_x)**2+(self.pos.y-init_y)**2)
            self.set_speed(x,0.0)
            rate.sleep()
        self.set_speed(0.0,0.0)
        
    def move_roll(self,theta,rad):
        rate=rospy.Rate(50)
        while((rad-self.pos.theta)**2>0.0004 ):
            self.set_speed(0.0,theta)
            rate.sleep()
        self.set_speed(0.0,0.0)
        
# if __name__ == '__main__':
#     turtle1 = Turtle1()
#     rospy.loginfo("start")
    
#     # turtle1.move_turtle1(0.2, 0.3, 5.0)
#     # turtle1.move_straight(-0.2,1.0)
#     turtle1.move_roll(0.2,180/math.pi*60)
#     rospy.loginfo("end")
if __name__ == '__main__':
    turtle1 = Turtle1()
    rospy.loginfo("start")
    turtle1.move_straight(0.2,1.0)
    turtle1.move_turtle1(0,0,0.5)
    turtle1.move_roll(0.5, math.pi/2)
    turtle1.move_turtle1(0,0,0.5)
    turtle1.move_straight(0.2,1.0)
    turtle1.move_turtle1(0,0,0.5)
    turtle1.move_roll(0.5, math.pi)
    turtle1.move_turtle1(0,0,0.5)
    turtle1.move_straight(0.2,1.0)
    turtle1.move_turtle1(0,0,0.5)
    turtle1.move_roll(0.5, -math.pi/2)
    turtle1.move_turtle1(0,0,0.5)
    turtle1.move_straight(0.2,1.0)
    turtle1.move_turtle1(0,0,0.5)
    turtle1.move_roll(0.5, 0)
    turtle1.move_turtle1(0,0,0.5)
    rospy.loginfo("end")