#!/usr/bin/env python

import rospy
from rospy import Subscriber, Publisher
from geometry_msgs.msg import Pose2D, Twist
from robot_control.controller import *

class ControllerNode:
  ''' Controller node
  '''
  def __init__(self,
               reference=[(-2.0, 0.0),
                          (-3.0, -1.0),
                          (0.0, 0.0)]):
    rospy.init_node("controller")
    rospy.sleep(0.5)

    self.controller = Controller()
    self.controller.start(reference)

    self.p = None

    self.pose_sub = Subscriber("state",
                               Pose2D,
                               self.on_pose)
    self.cmd_vel_pub = Publisher("twist_cmd",
                                 Twist,
                                 queue_size=10)

    self.run()

  def on_pose(self, pose):
    ''' Store the incoming new pose
    '''
    self.p = pose

  def run(self):
    ''' Main loop
    '''
    rate = rospy.Rate(10)
    t_start = rospy.Time.now().to_sec()

    while not rospy.is_shutdown():
      if self.controller.active:
        t = rospy.Time.now().to_sec() - t_start
        (v, w) = self.controller.generate_cmd(t, self.p)

        msg = Twist()
        msg.linear.x = v
        msg.angular.z = w
        self.cmd_vel_pub.publish(msg)

        rate.sleep()

