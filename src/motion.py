import ThunderBorg

LEFT = 'LEFT'
RIGHT = 'RIGHT'
BATTERY_MIN_VOLTAGE = 3.7 * 4
BATTERY_MAX_VOLTAGE = 4.2 * 4


def get_motor_name_error(function_name, motor_name):
	line_1 = 'Couldn\'t run ' + function_name + '.'
	line_2 = motor_name + ' is not a valid motor name!'
	line_3 = 'It must be either \'' + LEFT + '\' or \'' + RIGHT + '\'.'
	return line_1 + ' ' + line_2 + ' ' + line_3


def get_battery_percentage(current_voltage):
	battery_percentage = (current_voltage - BATTERY_MIN_VOLTAGE) / (BATTERY_MAX_VOLTAGE - BATTERY_MIN_VOLTAGE) 
	return battery_percentage


def normalize_speed(speed):
	return 0 if speed == 0.0 else speed


class Motors():
	def __init__(self):
		self.thunder_borg = ThunderBorg.ThunderBorg()
		self.thunder_borg.Init()
		self.thunder_borg.MotorsOff()

	def get_status(self):
		battery_voltage = self.thunder_borg.GetBatteryReading()
		battery_percentage = get_battery_percentage(battery_voltage)
		battery = {'voltage': battery_voltage, 'percent': battery_percentage}

		speed = {'left': self.get_speed(LEFT), 'right': self.get_speed(RIGHT)}

		return {'battery': battery, 'speed': speed}

	def get_speed(self, motor_name):
		if motor_name == LEFT:
			return normalize_speed(-self.thunder_borg.GetMotor1()) # Left motor is wired backwards!
		if motor_name == RIGHT:
			return normalize_speed(self.thunder_borg.GetMotor2())
		else:
			raise get_motor_name_error('get_speed()', motor_name)

	def set_speed(self, motor_name, speed):
		clamped_speed = min(1.0, max(-1.00, float(speed)))

		if motor_name == LEFT:
			self.thunder_borg.SetMotor1(-clamped_speed) # Left motor is wired backwards!
		elif motor_name == RIGHT:
			self.thunder_borg.SetMotor2(clamped_speed)
		else:
			self.stop()
			raise get_motor_name_error('set_speed(' + str(motor_name) + ', ' + str(speed) + ')', motor_name)

	def stop(self):
		self.thunder_borg.MotorsOff()

	def go(self, speed):
		self.set_speed(LEFT, speed)
		self.set_speed(RIGHT, speed)

	def turn(self, speed):
		self.set_speed(LEFT, -speed)
		self.set_speed(RIGHT, speed)

		