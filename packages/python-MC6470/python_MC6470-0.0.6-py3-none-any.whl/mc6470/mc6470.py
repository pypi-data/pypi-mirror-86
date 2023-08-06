import smbus
import time
import math

class Accelerometer():

	ADDR_A5_0 = 0x4C
	ADDR_A5_1 = 0x6C
	RESOLUTION_14_BIT = 0b101
	RANGE_8g = 0b010
	CONFIG_REG_ADDR = 0x20
	MODE_REG_ADDR = 0x07
	WAKE_UP_MODE = 0x01
	ACCL_DATA_REG_ADDR = 0x0D
	GRAVITATIONAL_ACCELERATION = 9.81

	def __init__(self,i2c_bus = 1,A5_state = 0,resolution = RESOLUTION_14_BIT,range = RANGE_8g):
		if A5_state == 0:
			self.address = Accelerometer.ADDR_A5_0
		else:
			self.address = Accelerometer.ADDR_A5_1
		self.bus = smbus.SMBus(i2c_bus)
		self.range = range
		self.resolution = resolution
		config = (range << 4) | resolution
		self.bus.write_byte_data(self.address,Accelerometer.CONFIG_REG_ADDR,config)
		self.bus.write_byte_data(self.address,Accelerometer.MODE_REG_ADDR,Accelerometer.WAKE_UP_MODE)
		time.sleep(0.1)

	@staticmethod
	def get_data_length_in_bits(resolution):
		switcher = {
			0: 6,
			1: 7,
			2: 8,
			3: 10,
			4: 12,
			5: 14,
		}
		return switcher.get(resolution)

	@staticmethod
	def get_angle_in_degrees(ax, ay):
		rad = math.atan2(ay,ax)
		deg = rad * (180.0/math.pi) + 180
		return deg

	def convert_digital_to_analog(self,digital_value):
		if(digital_value & 0x8000 > 0):
			analog_value = -(((~digital_value)&0xFFFF) + 1)
		else:
			analog_value = digital_value
		analog_value *= (2**(self.range + 1))*Accelerometer.GRAVITATIONAL_ACCELERATION/((2**(Accelerometer.get_data_length_in_bits(self.resolution) - 1)) - 1)
		return analog_value

	def get_data(self):
		data = self.bus.read_i2c_block_data(self.address,Accelerometer.ACCL_DATA_REG_ADDR,6)
		ax = ((data[1] << 8) | data[0])
		ax = self.convert_digital_to_analog(ax)
		ay = (data[3] << 8) | data[2]
		ay = self.convert_digital_to_analog(ay)
		az = (data[5] << 8) | data[4]
		az = self.convert_digital_to_analog(az)
		return (ax,ay,az)

