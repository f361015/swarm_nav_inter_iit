#!/usr/bin/env python3

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pubArr = None

class Listener:
  def __init__(self, index):
    self.index = index
  
  def take_action(self, regions):
    threshold_dist = 0.5
    linear_speed = 1.0
    angular_speed = 0.5

    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    if regions['front'] > threshold_dist and regions['left'] > threshold_dist and regions['right'] > threshold_dist:
      state_description = 'case 1 - no obstacle'
      linear_x = linear_speed
      angular_z = 0
    elif regions['front'] < threshold_dist and regions['left'] < threshold_dist and regions['right'] < threshold_dist:
      state_description = 'case 7 - front and left and right'
      linear_x = -linear_speed
      angular_z = angular_speed # Increase this angular speed for avoiding obstacle faster
    elif regions['front'] < threshold_dist and regions['left'] > threshold_dist and regions['right'] > threshold_dist:
      state_description = 'case 2 - front'
      linear_x = 0
      angular_z = angular_speed
    elif regions['front'] > threshold_dist and regions['left'] > threshold_dist and regions['right'] < threshold_dist:
      state_description = 'case 3 - right'
      linear_x = 0
      angular_z = -angular_speed
    elif regions['front'] > threshold_dist and regions['left'] < threshold_dist and regions['right'] > threshold_dist:
      state_description = 'case 4 - left'
      linear_x = 0
      angular_z = angular_speed
    elif regions['front'] < threshold_dist and regions['left'] > threshold_dist and regions['right'] < threshold_dist:
      state_description = 'case 5 - front and right'
      linear_x = 0
      angular_z = -angular_speed
    elif regions['front'] < threshold_dist and regions['left'] < threshold_dist and regions['right'] > threshold_dist:
      state_description = 'case 6 - front and left'
      linear_x = 0
      angular_z = angular_speed
    elif regions['front'] > threshold_dist and regions['left'] < threshold_dist and regions['right'] < threshold_dist:
      state_description = 'case 8 - left and right'
      linear_x = linear_speed
      angular_z = 0
    else:
      state_description = 'unknown case'
      rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pubArr[self.index-1].publish(msg)
  
  def callback_laser(self, msg):
    # 120 degrees into 3 regions
    regions = {
      'left':  min(min(msg.ranges[-60:-30]), 3.5),
      'front':  min(min(msg.ranges[:30]+msg.ranges[-30:0]), 3.5),
      'right':   min(min(msg.ranges[30:60]), 3.5),
    }
    self.take_action(regions)


def main():
  global pubArr
  
  n = 4
  rospy.init_node('reading_laser')

  pubArr = []
  subArr = []
  listenerArr = []
  
  for i in range(n):
    listenerArr.append(Listener(i+1))
    pubArr.append(rospy.Publisher("/robot"+str(i+1)+"/cmd_vel", Twist, queue_size=10))
    subArr.append(rospy.Subscriber("/robot"+str(i+1)+"/scan", LaserScan, listenerArr[i].callback_laser))
  
  rospy.spin()

if __name__ == '__main__':
  main()
