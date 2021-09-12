import socket
from socket import AF_INET, SOCK_DGRAM
from struct import unpack, calcsize
import matplotlib.pyplot as plt
from datetime import datetime
import time

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

fig = plt.figure()
plt.title("SMCU position updates", fontsize=26)
plt.xlabel("Time", fontsize=16)
plt.ylabel("Position", fontsize=16)
# plt.legend(loc="best", prop={"size": 10})
plt.tick_params(axis="both", which="major", labelsize=10)
plt.minorticks_on()
plt.grid(which="minor", linewidth=0.5, linestyle="--")
plt.grid(which="major", color="grey", linewidth=1)
plt.gcf().autofmt_xdate()

# Receive a new position updates broadcast protocol packet from SMCU model
while packet := s.recv(size):

    # Return a tuple containing integers. The integers refer to positions
    pos = unpack(payload_fmt, packet)

    magic, version, aposz1, aposz2, aposz3, lposx, lposy = pos

    # MAGIC is a constant '0xACDC', VERSION is a constant '0x0100'
    if magic != 0xACDC and version != 0x0100:
        continue

    print(
        f"APOSZ1: {aposz1}, APOSZ2: {aposz2}, APOSZ3: {aposz3}, \
LPOSX: {lposx}, LPOSY: {lposy}"
        )

    time = datetime.now()
    plt.scatter(time, aposz1, s=50)
    plt.scatter(time, aposz2, s=50)
    plt.scatter(time, aposz3, s=50)
    plt.scatter(time, lposx, s=50)
    plt.scatter(time, lposy, s=50)
    plt.pause(0.00001)
