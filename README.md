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
After that make sure that you have sourced your workspace after which you can have a quick demonstration of task-allocation using this video...


https://github.com/user-attachments/assets/d6b1469f-3b1b-465d-8b75-e72a5bb1f59f


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
Here roomba.py is a test file which produces a motion while detecting obstacles for individual robots independently.

By deafult, the simulation opens with a premade map for the pre-loaded house map, However there are many different worlds provided by the turtlebot3 package which we have used extensively for using their "Waffle_Pi" robot model and their inbuilt environments. The map is by default saved in the map folder of the turtlebot3_navigation folder but it can be stored anywhere, you just need to chage the launch files accordingly.

For eg. if you don't want to load a preloaded map then you can the comment the map_server node (i.e. lines 4 to 6 in 'navigation.launch') and just before launching the 'navigation.launch' file make sure to launch the 'map_merge.launch' to simultaniously map the environment as you go.
```xml

<node name="map_server" pkg="map_server" type="map_server" args="$(find swarm_nav_inter_iit)/turtlebot3/turtlebot3_navigation/maps/map.yaml">
        <param name="frame_id" value="map"/>
</node>

<!-- <node name="map_server" pkg="map_server" type="map_server" args="$(find swarm_nav_inter_iit)/turtlebot3/turtlebot3_navigation/maps/map.yaml">
        <param name="frame_id" value="map"/>
</node> -->
```
