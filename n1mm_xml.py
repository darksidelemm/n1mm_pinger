#!/usr/bin/env python
#
#	N1MM Broadcast XML Parser
#
#	Decode N1MM Broadcast XML data
#	Refer: http://n1mm.hamdocs.com/tiki-index.php?page=UDP+Broadcasts
#
#   Mark Jessop <vk5qi@rfhead.net> 2017-09  
#
import xml.etree.ElementTree as ET


N1MM_VALID_TAGS = ['contactinfo', 'RadioInfo']


def parse_n1mm_packet(data):
	""" 
	Attempt to parse a XML packet, send by N1MM.

	Returns a dictionary if successful.
	"""

	data = ET.fromstring(data)

	if data.tag not in N1MM_VALID_TAGS:
		raise IOError("Invalid packet type.")

	# Start populating an output dictionary.
	output = {}
	output['type'] = data.tag

	output['fields'] = {}
	for child in data:
		output['fields'][child.tag] = child.text

	return output





if __name__ == "__main__":
	f = open('n1mm_contact.xml','r')
	data = f.read()
	f.close()

	print(parse_n1mm_packet(data))