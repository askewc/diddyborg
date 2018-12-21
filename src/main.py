#!/usr/bin/env python

import time

import distance
import motion


def main():
	sensors = distance.Sensors()
	motors = motion.Motors()
	
	initial_distances = sensors.read()

	motors.go(50)

	for i in range(60):
		current_distances = sensors.read()
		
		if any(d <= 300 and d != 0 for d in current_distances):
			break

		time.sleep(.25)


	motors.stop()
	time.sleep(1)

	current_distances = sensors.read()
	delta_distances = [current - initial for initial, current in zip(initial_distances, current_distances)]

	print('delta_distances', delta_distances)





if __name__ == '__main__':
	main()
