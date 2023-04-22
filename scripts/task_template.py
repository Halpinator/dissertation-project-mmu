#!/usr/bin/env python3

import rospy
from task import Task
from task_handler import TaskHandler

def main():
    rospy.init_node('task_template_node')

    rospy.sleep(3)  # Add a delay of 3 seconds

    task_handler = TaskHandler()

    task_handler.add_task(Task('move forwards', 5))
    task_handler.add_task(Task('turn right', 2))
    task_handler.add_task(Task('move forwards', 5))
    task_handler.add_task(Task('speak', 3, "Hello, my name is " + rospy.get_param("robot_name")))

    rospy.spin()

if __name__ == '__main__':
    main()
