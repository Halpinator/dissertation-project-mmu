#!/usr/bin/env python3

import rospy
from task import Task
from task_handler import TaskHandler

def main():
    rospy.init_node('task_template_node')

    task_handler = TaskHandler()

    task_handler.add_task(Task('forward', 2))
    task_handler.add_task(Task('right', 1))
    task_handler.add_task(Task('forward', 5))
    task_handler.add_task(Task('speak', 3, "Hello, this is an example message."))

    rospy.spin()

if __name__ == '__main__':
    main()
