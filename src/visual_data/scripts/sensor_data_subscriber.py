#!/usr/bin/env python3

import rospy
from visual_data.msg import sensor_data_message

def sensor_data_callback(sensor_data_message):
    rospy.loginfo(
        "Gauti duomenys: (%d, %s, %.3f, %.3f, %.3f)",
        sensor_data_message.id,
        sensor_data_message.name,
        sensor_data_message.x,
        sensor_data_message.y,
        sensor_data_message.z)

rospy.init_node('sensor_data_subscriber', anonymous = True)

rospy.Subscriber("sensor_data_stream", sensor_data_message, sensor_data_callback)

rospy.spin()
