import rospy
from geometry_msgs.msg import Twist

class turtlebot_controller():
    def __init__(self):
        rospy.init.node('Turtlebot_control_node', anonymous=True)

        rospy.loginfo('To stop turtlebot, press ctrl+c')
        rospy.on_shutdown(self.shutdown)

        self.cmd_vel_object = rospy.Publisher('', msg_type, queue_size=)


    def shutdown((self)):
        #shutdown code
        

    if __name__ == '__main__':
        try:
            turtlebot_controller()
        except:
            rosp.loginfo('Node Terminated')