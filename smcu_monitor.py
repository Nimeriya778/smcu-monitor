import socket
from socket import AF_INET, SOCK_DGRAM
from struct import unpack, calcsize

# Create a socket object
s = socket.socket(family=AF_INET, type=SOCK_DGRAM, proto=0)

# Listen address
host = "127.0.0.1"

# Reserve a port for UDP protocol
UDP_PORT = 20817

s.bind((host, UDP_PORT))

# The UDP diagram payload has data fields described in struct format
payload_fmt = '>HH5i'
size = calcsize(payload_fmt)

# Receive a new position updates broadcast protocol packet from SMCU model
while packet := s.recv(size):

    # Return a tuple containing integers. The integers refer to positions
    pos = unpack(payload_fmt, packet)

    magic, version, aposz1, aposz2, aposz3, lposx, lposy = pos

    # MAGIC is a constant '0xACDC', VERSION is a constant '0x0100'
    if magic == 44252 and version == 256:

        print(
            f"APOSZ1: {aposz1}, APOSZ2: {aposz1}, APOSZ3: {aposz3}, \
LPOSX: {lposx}, LPOSY: {lposy}"
            )
