#!/usr/bin/env python3

import math as m
import numpy as np
import time
import socket
import pandas as pd
import rospy
from visual_data.msg import sensor_data_message

TCP_IP = '192.168.1.118'
TCP_PORT = 4001
BUFFER_SIZE = 13
net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
net.connect((TCP_IP, TCP_PORT))
net.setblocking(False)

q_deg_real = [0,0,0,0,0,0,0,0,0,0,0,0,0] #q0, q1, q2, q3
q_deg_memory = np.empty([0,13])

def read_sensor():
	global q_deg_real
	global q_deg_memory
	angle_mem = 0
	sensor_data = [None, None, None, None]
	while True:
		try:
			data = net.recv(BUFFER_SIZE)
			if len(data) == 13:
				#print(data)
				ID = data[4]
				if ID == 80:
					sensor_data[0] = data
				elif ID == 81:
					sensor_data[1] = data
				elif ID == 82:
					sensor_data[2] = data
				elif ID == 84:
					sensor_data[3] = data
			if (sensor_data[0] != None and sensor_data[1] != None and sensor_data[2] != None and sensor_data[3] != None) == True:
				break
		except:
			pass
	
	try:
		data_flush = net.recv(130)
		print("buffer flushed")
	except:
		pass
	
	q_deg_real[0] = round(np.short(sensor_data[0][8] << 8 | sensor_data[0][7]) / 32768.0 * 180,2)
	q_deg_real[1] = round(np.short(sensor_data[0][10] << 8 | sensor_data[0][9]) / 32768.0 * 180,2)
	q_deg_real[2] = round(np.short(sensor_data[0][12] << 8 | sensor_data[0][11]) / 32768.0 * 180,2)
	q_deg_real[3] = -round(np.short(sensor_data[1][8] << 8 | sensor_data[1][7]) / 32768.0 * 180,2)
	q_deg_real[4] = round(np.short(sensor_data[1][10] << 8 | sensor_data[1][9]) / 32768.0 * 180,2)
	q_deg_real[5] = round(np.short(sensor_data[1][12] << 8 | sensor_data[1][11]) / 32768.0 * 180,2)
	q_deg_real[6] = -round(np.short(sensor_data[2][8] << 8 | sensor_data[2][7]) / 32768.0 * 180,2)
	q_deg_real[7] = round(np.short(sensor_data[2][10] << 8 | sensor_data[2][9]) / 32768.0 * 180,2)
	q_deg_real[8] = round(np.short(sensor_data[2][12] << 8 | sensor_data[2][11]) / 32768.0 * 180,2)
	q_deg_real[9] = round(np.short(sensor_data[3][8] << 8 | sensor_data[3][7]) / 32768.0 * 180,2)
	q_deg_real[10] = round(np.short(sensor_data[3][10] << 8 | sensor_data[3][9]) / 32768.0 * 180,2)
	q_deg_real[11] = round(np.short(sensor_data[3][12] << 8 | sensor_data[3][11]) / 32768.0 * 180,2)
	
	q_deg_memory = np.append(q_deg_memory, [q_deg_real], 0)

pub = rospy.Publisher('sensor_data_stream', sensor_data_message, queue_size = 10)

rospy.init_node('sensor_data_publisher', anonymous = True)

rate = rospy.Rate(10)

i = 0
while not rospy.is_shutdown():
    read_sensor()
    
    gyro50 = sensor_data_message()
    gyro50.id = 50
    gyro50.name = "0_x50"
    gyro50.x = q_deg_real[0]
    gyro50.y = q_deg_real[1]
    gyro50.z = q_deg_real[2]
    
    gyro51 = sensor_data_message()
    gyro51.id = 51
    gyro51.name = "0_x51"
    gyro51.x = q_deg_real[3]
    gyro51.y = q_deg_real[4]
    gyro51.z = q_deg_real[5]

    gyro52 = sensor_data_message()
    gyro52.id = 52
    gyro52.name =  "0_x52"
    gyro52.x = q_deg_real[6]
    gyro52.y = q_deg_real[7]
    gyro52.z = q_deg_real[8]

    gyro54 = sensor_data_message()
    gyro54.id = 54
    gyro54.name = "0_x54"
    gyro54.x = q_deg_real[9]
    gyro54.y = q_deg_real[10]
    gyro54.z = q_deg_real[11]

    rospy.loginfo("Siunciami duomenys: ")
    rospy.loginfo(gyro50)
    pub.publish(gyro50)

    rospy.loginfo(gyro51)
    pub.publish(gyro51)

    rospy.loginfo(gyro52)
    pub.publish(gyro52)

    rospy.loginfo(gyro54)
    pub.publish(gyro54)
	
    rate.sleep()
    i = i + 1