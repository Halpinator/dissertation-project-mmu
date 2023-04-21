# task_handler.py

import rospy
import threading
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from task import Task

class TaskHandler:
    def __init__(self):
        self.task_queue = []
        self.is_executing = False
        self.move_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.speak_pub = rospy.Publisher('/voice_commands', String, queue_size=10)

    def add_task(self, task):
        self.task_queue.append(task)
        if not self.is_executing:
            self.execute_tasks()

    def execute_tasks(self):
        if not self.task_queue:
            self.is_executing = False
            return

        self.is_executing = True
        task = self.task_queue.pop(0)
        if task.task_type in ['forward', 'back', 'left', 'right', 'stop']:
            self.execute_move_task(task)
        elif task.task_type == 'speak':
            self.execute_speak_task(task)
        else:
            rospy.loginfo("Invalid task type")

    def execute_move_task(self, task):
        cmd = self.move_command(task.task_type)
        self.move_pub.publish(cmd)
        rospy.sleep(task.duration)
        self.move_pub.publish(Twist())  # stop movement
        self.execute_tasks()

    def execute_speak_task(self, task):
        self.speak_pub.publish(task.message)
        rospy.sleep(task.duration)
        self.execute_tasks()

    @staticmethod
    def move_command(text):
        cmd = Twist()
        if text == 'forward':
            cmd.linear.x = 0.25
        elif text == 'back':
            cmd.linear.x = -0.25
        elif text == 'left':
            cmd.angular.z = 0.25
        elif text == 'right':
            cmd.angular.z = -0.25
        elif text == 'stop':
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
        return cmd
