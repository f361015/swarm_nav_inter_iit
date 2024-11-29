#!/usr/bin/env python3

import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped

taskLocations = None

class moveBaseClient:
  def __init__(self, index, singlerobotQueue):
    self.index = index
    self.queue = singlerobotQueue
    self.reach_goal()

  def reach_goal(self):
    client = actionlib.SimpleActionClient('robot'+str(self.index+1)+'/move_base',MoveBaseAction)
    client.wait_for_server()

    if self.queue == []:
      return
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = taskLocations[self.queue[0]][0]
    goal.target_pose.pose.position.y = taskLocations[self.queue[0]][1]
    goal.target_pose.pose.orientation.w = 1
    client.send_goal(goal)
    return client.get_result()
  
  def take_action(self, regions):
    msg = PoseStamped()
  
  def callback_laser(self, msg):
    self.take_action()


def main():
  global taskLocations

  n = 4
  taskL = open('task_locations.txt', "r").readlines()
  taskQueue = open('task_queue.txt', "r").read().split()
  taskLocations = {}
  for i in taskL:
    tmp = i.split()
    taskLocations.update({tmp[0]: list((float(tmp[1]), float(tmp[2])))})

  robotQueue = [[] for i in range(n)]

  for i in range(len(taskQueue)):
    ind = i%n
    robotQueue[ind].append(taskQueue[i])

  rospy.init_node('tasks')
  
  moveBaseClients = [moveBaseClient(i, robotQueue[i]) for i in range(n)]

  rospy.spin()

if __name__ == '__main__':
  main()