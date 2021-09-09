import socket
from socket import AF_INET, SOCK_DGRAM
from struct import *

# Create a socket object
s = socket.socket(family=AF_INET, type=SOCK_DGRAM, proto=0)

# Listen address
host = "127.0.0.1"

# Reserve a port for UDP protocol
UDP_PORT = 20817

s.bind((host, UDP_PORT))

# The UDP diagram payload has the following data fields sizes

# Constant '0xACDC'
MAGIC_SZ = 2

# Constant '0x0100'
VERSION_SZ = 2

# Angular Z1 position
APOSZ1_SZ = 4

# Angular Z2 position
APOSZ2_SZ = 4

# Angular Z3 position
APOSZ3_SZ = 4

# Linear X position
LPOSX_SZ = 4

# Linear Y position
LPOSY_SZ = 4

# Data fields offsets
APOSZ1_OFF = 4
APOSZ2_OFF = 8
APOSZ3_OFF = 12
LPOSX_OFF = 16
LPOSY_OFF = 20

# Receive a new position updates broadcast protocol packet from SMCU model
while packet := s.recv(24):

    # Return a tuple containing integers. The integers refer to positions
    pos = unpack('>5i', packet[4:25])

    print(
        f"APOSZ1: {pos[0]}, APOSZ2: {pos[1]}, APOSZ3: {pos[2]}, \
LPOSX: {pos[3]}, LPOSY: {pos[4]}"
        )
