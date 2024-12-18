# Centralized Intelligence for Dynamic Swarm Navigation (BharatForge)

This Project was made under a week for an Inter IIT TechMeet 13.0 Robotics Problem Statement

_Apologies if the project is a bit wonky, it was my first time with ros, robotics and this field in general. Plus, its highly unlikely that I'll keep updating this repository but I will polish it up for github once the event is over._

## Problem Statement

The problem focuses on designing a Singular Brain for a robot swarm tasked with performing optimized path planning in highly dynamic environments. The challenges involve developing and training a multi-agent system capable of navigating in environments where:
* **No GPS** is available.
* **Frequent and unpredictable changes occur**, such as moving obstacles or rearranged objects.

The robot swarm must collaboratively plan the optimal path to accomplish a set of tasks while avoiding collisions and delays. Efficiency is critical, requiring:
* Dynamic **ranking of navigation tasks** based on travel time.
* **Memory persistence**, where robots label and store dynamic changes in the environment in a shared, continuously updating database.
  
The ideal solution should be:
* **Scalable**, maintaining efficiency even in new, larger environments with additional robots.
* **Adaptable**, enabling the swarm to autonomously explore any environment and create a dynamic database/map of object locations without manual intervention.

The ultimate objective is to develop a software solution capable of ensuring optimal swarm performance, even under highly dynamic and complex conditions.

![Screenshot from 2024-12-01 00-40-41](https://github.com/user-attachments/assets/e269155c-7f04-4f04-aa6a-09f65ffe2236)

***
## How to run this package?
First make sure you have installed all the dependencies and the required packages for this project... i.e
1. **gazebo** (For simulation)
2. **rviz** (For visualization)
3. **map_server** (If you want to use a preloaded server)
4. **gmapping** (for mapping the environment)
5. **amcl** (For localisation)
6. **move_base** (For navigation and both local and global path planning)
7. **map_merge** (To merge maps; _make sure to have good odometry before trying this_)
8. **explore_lite** (If you want to explore)

The Python dependencies for running the YOLO model can be installed by:
```
pip install ultralytics opencv-python numpy
```

Don't worry, if you forget to install the dependency then ros will notify you after which you can install that specfic file.
> [!NOTE]
> Due to us not managing the package.xml and CMakeLists.txt, using `rosdep` might not work.

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
$ rosrun swarm_nav_inter_iit task_allocator.py
```
You can change the locations of the tasks in `task_locations.txt` and the task queue in `task_queue.txt` both of which are in the 'scripts' folder.

Here roomba.py is a test file which produces a  random motion while detecting obstacles for individual robots independently.

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

This will give map to the `/map` topic in gazebo.

To add and remove robots from the environment you'll have to copy and paste this in the `swarm.launch` with the appropriate number.

Note that we are using turtlebot3 extensively but with enough changes you can make it so that it incorporates any robot you want.

> [!IMPORTANT]
> Keep the initial namespace as 'robot' and the numbers increasing because the python script assumes the robots are named as "robot1", "robot2" etc...

```xml
    <group ns="robot5">
        <param name="tf_prefix" value="robot2"/>
        <include file="$(find swarm_nav_inter_iit)/launch/single.launch" >
            <arg name="init_pose" value="-x -1 -y 3.5 -z 0" />
            <arg name="model" value="waffle_pi" />
            <arg name="multi_robot_name" value="robot5" />
        </include>
    </group>
```
Then configure `move_base` and `amcl` launch files for every robot in the corresponding folder by which you can configure ther parameters, namespaces etc. Then add the includes in the `navigation.launch` file.
```xml
<include file="$(find swarm_nav_inter_iit)/launch/amcl_swarm/amcl_robot5.launch" />

<include file="$(find swarm_nav_inter_iit)/launch/move_base_swarm/move_base_robot5.launch"/>
```

By default, the `costmap_common_params` are stored in `turtlebot3/turtlebot3_navigation/param/cost_common_params` folder.

In order to turn on YOLO at any stage of running this, just run the `yolo.py` script
```
$ rosrun swarm_nav_inter_iit yolo.py
```

The processed images are published in the `/robot{id}/camera/rgb/image_processed` topic


https://github.com/user-attachments/assets/3b133f1e-d37c-439a-83b6-19b495bc9729


> [!NOTE]
> Here we are using the `yolo11n.pt` weights, you can use others as well.

***
## Demonstrations
The followings are Trimmed and Sped up demonstrations of the videos uploaded in `DEMO_VIDEOS`:

* Environment- House ; Robots- 4 ; Exploring map autonomously


https://github.com/user-attachments/assets/70404d48-629c-46f0-a625-c3d2ac16b919


* Environment- House ; Robots- 4 ; Naviagting tasks in `task_queue`


https://github.com/user-attachments/assets/58d6ab63-5afa-4efe-b3c2-dea5efaf7688


* Environment- Warehouse ; Robots- 9 ; Exploring map in via `explore_lite` and `map_merge`


https://github.com/user-attachments/assets/611cfb48-2eff-464d-ba3a-ed47551ca513


* Environment- Warehouse ; Robots- 9 ; Navigating tasks in `task_queue.txt` and `YOLO` Detection


https://github.com/user-attachments/assets/c47c89de-f278-48f2-8568-1d9182d71b0a


