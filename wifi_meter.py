#!/usr/bin/env python
#	
#	SpeakerPhat VU Display - WiFI Signal Meter
#	Used to check wifi range when setting up for the OCDX Amateur Radio contest.
#	This script reads the wifi link quality from iwconfig, and displays the level
#	on the speaker-phat V/U display LEDs.
#
#	Doesn't really belong in this repo, but it's running on the same device, so whatever :-)
#
#   Mark Jessop <vk5qi@rfhead.net> 2017-09  
#
import subprocess
import time
from speakerphat import set_led, show


def read_iwconfig():
	"""
	Read from iwconfig, and attempt to parse out the link quality value.
	Scale link quality to a single float between 0-1.0 and return.
	"""

	data = subprocess.check_output(['iwconfig'])

	for line in data.split('\n'):
		if 'Link Quality' in line:
			lq_data = line.split('=')[1].split('  ')[0]
			lq_level = float(lq_data.split('/')[0])
			lq_max = float(lq_data.split('/')[1])
			return lq_level/lq_max

	return 0.0


def convert_float(value):
	"""
	Display a floating point value on the SpeakerPhat LEDs.
	"""

	# Clip input
	if value > 1.0:
		value = 1.0

	if value < 0.0:
		value = 0.0

	# We need to convert the input value to a 10-long array of values between 0-255.
	# i.e. 0.0 would result in [0,0,..,0,0]
	# 0.1 would result in [255,0,0...0,0]
	# and so on

	# output array
	output = [0,0,0,0,0,0,0,0,0,0]

	value = value * 10.0

	for n in range(0,10):
		remainder = value - float(n)
		if remainder > 1.0:
			output[n-1] = 255
		elif remainder < 0.0:
			output[n-1] = 0
		else:
			output[n-1] = int(remainder*255)

	return output


def display_array(data):
	"""
	Display a 10-element array of 0-255 values on the speakerphat display
	"""

	for n in range(0,10):
		set_led(n,data[n])
	show()



if __name__ == "__main__":
	while True:
		try:
			value = read_iwconfig()
		except:
			value = 0.0

		display_array(convert_float(value))
		time.sleep(0.5)


