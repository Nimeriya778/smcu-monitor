import socket
from socket import AF_INET, SOCK_DGRAM

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
while packet := bytes(s.recv(24)):

    # Receive positions values in bytes
    aposz1 = packet[APOSZ1_OFF: APOSZ1_OFF + APOSZ1_SZ]
    aposz2 = packet[APOSZ2_OFF: APOSZ2_OFF + APOSZ2_SZ]
    aposz3 = packet[APOSZ3_OFF: APOSZ3_OFF + APOSZ3_SZ]
    lposx = packet[LPOSX_OFF: LPOSX_OFF + LPOSX_SZ]
    lposy = packet[LPOSY_OFF: LPOSY_OFF + LPOSY_SZ]

    # Create an int from bytes
    i_aposz1 = int.from_bytes(aposz1, byteorder="big", signed=True)
    i_aposz2 = int.from_bytes(aposz2, byteorder="big", signed=True)
    i_aposz3 = int.from_bytes(aposz3, byteorder="big", signed=True)
    i_lposx = int.from_bytes(lposx, byteorder="big", signed=True)
    i_lposy = int.from_bytes(lposy, byteorder="big", signed=True)

    print(
        f"APOSZ1: {i_aposz1}, APOSZ2: {i_aposz2}, APOSZ3: {i_aposz3}, \
LPOSX: {i_lposx}, LPOSY: {i_lposy}"
        )
#     print(
#         f"Bytes --> APOSZ1: {aposz1}, APOSZ2: {aposz2}, APOSZ3: {aposz3}, \
# LPOSX: {lposx}, LPOSY: {lposy}"
#         )