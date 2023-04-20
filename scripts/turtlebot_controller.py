#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def turtlebot3_spin():
    rospy.init_node('turtlebot3_spin', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        spin_msg = Twist()
        spin_msg.linear.x = 0.0
        spin_msg.linear.y = 0.0
        spin_msg.linear.z = 0.0
        spin_msg.angular.x = 0.0
        spin_msg.angular.y = 0.0
        spin_msg.angular.z = 1.0  # Positive value will make the robot spin clockwise

        pub.publish(spin_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        turtlebot3_spin()
    except rospy.ROSInterruptException:
        pass