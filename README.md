First, clone this repo in a workspace's src folder.
```
$ git clone https://github.com/f361015/swarm_nav_inter_iit.git
```
Now make sure to catkin_make or catkin build the workspace.
```
$ catkin_make
```
In order to start a gazebo simulaton run the main.launch file
```
$ roslaunch swarm_nav_inter_iit main.launch
```
In order to start navigation start the navigation.launch file
```
$ roslaunch swarm_nav_inter_iit navigation.launch
```
In order to run any python script in the simulation do-
```
$ rosrun swarm_nav_inter_iit roomba.py
```
Here roompy.py is a test file which produces a motion while detecting obstacles.
