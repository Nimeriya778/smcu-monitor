#!/usr/bin/env python

"""
Receives position updates via UDP
"""

from socket import socket, AF_INET, SOCK_DGRAM
from struct import unpack, calcsize
from datetime import datetime
from matplotlib import pyplot as plt

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

time_log, z1_log, z2_log, z3_log, x_log, y_log = [], [], [], [], [], []

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

        # Save logs to plot data
        time = datetime.now()
        time_log.append(time)
        z1_log.append(aposz1)
        z2_log.append(aposz2)
        z3_log.append(aposz3)
        x_log.append(lposx)
        y_log.append(lposy)

except KeyboardInterrupt:
    print("\nStopped by user")

# Creating multiple plots
fig, ax = plt.subplots()

# Plot settings
plt.title("SMCU position updates", fontsize=26)
plt.xlabel("Time", fontsize=16)
plt.ylabel("Position", fontsize=16)
plt.tick_params(axis="both", which="major", labelsize=10)
plt.minorticks_on()
plt.grid(which="minor", linewidth=0.5, linestyle="--")
plt.grid(which="major", color="grey", linewidth=1)
plt.gcf().autofmt_xdate()

ax.plot(time_log, z1_log, ".-", label="APOSZ1")
ax.plot(time_log, z2_log, ".-", label="APOSZ2")
ax.plot(time_log, z3_log, ".-", label="APOSZ3")
ax.plot(time_log, x_log, ".-", label="LPOSX")
ax.plot(time_log, y_log, ".-", label="LPOSY")

# Display plots
plt.legend(loc="best")
plt.show()
