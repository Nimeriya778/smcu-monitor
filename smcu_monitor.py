#!/usr/bin/env python

"""
Receives position updates via UDP
"""

from socket import socket, AF_INET, SOCK_DGRAM
from struct import unpack, calcsize

# Listen address
DEFAULT_HOST = "127.0.0.1"

# Reserve a port for UDP protocol
UDP_PORT = 20817

# Create a socket object
s = socket(family=AF_INET, type=SOCK_DGRAM, proto=0)

s.bind((DEFAULT_HOST, UDP_PORT))

# The UDP diagram payload has data fields described in struct format
PAYLOAD_FMT = ">HH5i"
size = calcsize(PAYLOAD_FMT)

try:
    # Receive a new position updates broadcast protocol packet from SMCU model
    while packet := s.recv(size):

        # Return a tuple containing integers. The integers refer to positions
        pos = unpack(PAYLOAD_FMT, packet)

        magic, version, aposz1, aposz2, aposz3, lposx, lposy = pos

        # MAGIC is a constant '0xACDC', VERSION is a constant '0x0100'
        if magic != 0xACDC and version != 0x0100:
            continue
        print(
            f"APOSZ1: {aposz1}, APOSZ2: {aposz2}, APOSZ3: {aposz3}, \
LPOSX: {lposx}, LPOSY: {lposy}"
        )
except KeyboardInterrupt:
    print("\nStopped by user")
