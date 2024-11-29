First make sure you have installed all the dependencies and the required packages for this project... i.e
1. **gazebo** (For simulation)
2. **rviz** (For visualization)
3. **map_server** (If you want to use a preloaded server)
4. **gmapping** (for mapping the environment)
5. **amcl** (For localisation)
6. **move_base** (For navigation and both local and global path planning)
7. **map_merge** (To merge maps; _make sure to have good odometry before trying this_)
8. **explore_lite** (If you want to explore)
Don't worry, if you forget to install the dependency then ros will notify you after which you can install that specfic file. (_Note that due to us not managing the package.xml and CMakeLists.txt, using rosdep might not work_)
Then, clone this repo in a workspace's src folder.
```
$ git clone https://github.com/f361015/swarm_nav_inter_iit.git
```
Now make sure to catkin_make or catkin build the workspace.
```
$ catkin_make
```
After that make sure that you have sourced your workspace after which you can have a quick demonstration of task allocation using this video...

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
