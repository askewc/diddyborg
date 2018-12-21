import time

from backend.lib import UltraBorg


class Sensors:
	def __init__(self):
		self.ultra_borg = UltraBorg.UltraBorg()
		self.ultra_borg.Init()

	def read(self):
		distance1 = self.ultra_borg.GetDistance1()
		time.sleep(.01)
		distance1 = int((distance1 + self.ultra_borg.GetDistance1()) / 2.0)

		time.sleep(.01)

		distance2 = self.ultra_borg.GetDistance2()
		time.sleep(.01)
		distance2 = int((distance2 + self.ultra_borg.GetDistance2()) / 2.0)

		time.sleep(.01)

		distance3 = self.ultra_borg.GetDistance3()
		time.sleep(.01)
		distance3 = int((distance3 + self.ultra_borg.GetDistance3()) / 2.0)

		time.sleep(.01)

		distance4 = self.ultra_borg.GetDistance4()
		time.sleep(.01)
		distance4 = int((distance4 + self.ultra_borg.GetDistance4()) / 2.0)

		return distance1, distance2, distance3, distance4
