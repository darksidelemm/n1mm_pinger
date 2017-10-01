#!/usr/bin/env python
#
#   The Python Script that goes Ping!
#
#   Go PING! whenever someone makes a contact!
#
#   Mark Jessop <vk5qi@rfhead.net> 2017-09   
#
from n1mm_xml import *
import subprocess
import socket

# What port N1MM is sending UDP broadcast packets to.
N1MM_UDP_PORT = 12060

# What command to run when a contact packet is received.
PING_CMD = "play ping.wav"


def ping():
    """
    PING!
    """
    subprocess.call(PING_CMD, shell=True)


def process_udp(packet):
    """
    Attempt to parse the received data.
    """
    try:
        data = parse_n1mm_packet(packet)
    except:
        print("Invalid packet.")

    if data['type'] == 'contactinfo':
        ping()


def udp_rx_thread():
    """ 
    Listen for Broadcast UDP packet in port 12060 (N1MM broadcast default).
    """
    global udp_listener_running
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(0.2)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except:
        pass
    s.bind(('',N1MM_UDP_PORT))
    print("Started UDP Listener Thread.")
    udp_listener_running = True
    while udp_listener_running:
        try:
            (m,addr) = s.recvfrom(2048)
            print(addr)
        except socket.timeout:
            m = None
        
        if m != None:
                process_udp(m)
    
    print("Closing UDP Listener")
    s.close()


if __name__ == "__main__":
    try:
        udp_rx_thread()
    except KeyboardInterrupt:
        print("Closing.")