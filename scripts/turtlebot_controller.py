#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def move_command(text):
    cmd = Twist()
    if text == 'move forwards':
        cmd.linear.x = 0.2
    elif text == 'move backwards':
        cmd.linear.x = -0.2
    elif text == 'turn left':
        cmd.angular.z = 0.2
    elif text == 'turn right':
        cmd.angular.z = -0.2
    elif text == 'stop':
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
    return cmd

def callback(msg):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    text = msg.data
    cmd = move_command(text)
    pub.publish(cmd)

def main():
    rospy.init_node('turtlebot_controller_node')
    rospy.Subscriber('/voice_commands', String, callback)
    rospy.spin()

if __name__ == '__main__':
    main()