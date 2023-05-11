ROS version: Noetic
OS: Ubuntu Linux
Language: Python

Global wake word: ALEXA


//To open gazebo
export TURTLEBOT3_MODEL=burger
roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch

//Run this to run the test voice control and task code
roslaunch dissertation-project-mmu turtlebot_voice_control.launch

//Run this to run the task template 
rosrun dissertation-project-mmu task_template.py
