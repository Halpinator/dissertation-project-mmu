# task_handler.py

import rospy
import threading
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from task import Task
from turtlebot_controller import move_command

class TaskHandler:
    def __init__(self):
        self.task_queue = []
        self.is_executing = False
        self.move_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.speak_pub = rospy.Publisher('/voice_commands', String, queue_size=10)
        self.wait_for_connection()

    def wait_for_connection(self):
        while self.move_pub.get_num_connections() < 1 or self.speak_pub.get_num_connections() < 1:
            rospy.sleep(0.1)

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
        if task.task_type in ['move forwards', 'move backwards', 'turn left', 'turn right', 'stop']:
            self.execute_move_task(task)
        elif task.task_type == 'speak':
            self.execute_speak_task(task)
        else:
            rospy.loginfo("Invalid task type")

    def execute_move_task(self, task):
        cmd = move_command(task.task_type)
        self.move_pub.publish(cmd)
        rospy.sleep(task.duration)
        self.move_pub.publish(Twist())  # stop movement
        rospy.sleep(0.5)  # Add a short delay to allow the robot to settle
        self.execute_tasks()

    def execute_speak_task(self, task):
        self.speak_pub.publish(task.message)
        rospy.sleep(task.duration)
        self.execute_tasks()
    
        
