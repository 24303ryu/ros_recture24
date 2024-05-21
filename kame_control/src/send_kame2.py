#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import dynamic_reconfigure.client


class SimpleGoal:
    def __init__(self):
        self.way_points = [
            [-6.0,-3.0,0],
            [7.0,4.0,0],
            [6.0,-6.0,0],
        ]
        
        rospy.init_node('simple_goal')
        self.pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=2)

        # Set initial position
        init_pose = PoseWithCovarianceStamped()
        init_pose.header.stamp = rospy.Time.now()
        init_pose.header.frame_id = 'map'
        init_pose.pose.pose.position.x = -3.0
        init_pose.pose.pose.position.y = 1.0
        init_pose.pose.pose.position.z = 0
        init_pose.pose.pose.orientation.w = 1.0

        self.pub.publish(init_pose)
        rospy.sleep(1)
        self.pub.publish(init_pose)
        
        self.ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Waiting for the move_base action server to come up")
        self.ac.wait_for_server(rospy.Duration(5.0))
        rospy.loginfo("The server comes up")
        
        self.client = dynamic_reconfigure.client.Client("move_base/DWAPlannerROS")
        self.client.update_configuration({"max_vel_x": 100.0, "max_vel_theta": 10.0})

    def send_goal(self, x, y, yaw):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.w = 1.0

        rospy.loginfo("Sending goal: x=%.2f, y=%.2f, yaw=%.2f", x, y, yaw)
        self.ac.send_goal(goal)

        succeeded = self.ac.wait_for_result(rospy.Duration(1000.0))
        state = self.ac.get_state()

        if succeeded:
            rospy.loginfo("Succeeded: (%s)", state)
        else:
            rospy.loginfo("Failed: (%s)", state)

    def run(self):
        i = 0
        while not rospy.is_shutdown():
            x, y, yaw = self.way_points[i]
            print(x,y,yaw)
            self.send_goal(x, y, yaw)
            i += 1


if __name__ == '__main__':
    try:
        simple_goal = SimpleGoal()
        simple_goal.run()
    except rospy.ROSInterruptException:
        pass
