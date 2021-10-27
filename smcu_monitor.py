#!/usr/bin/env python

"""
Receives position updates via UDP
"""

import argparse
import csv
from datetime import datetime, timedelta
from socket import socket, AF_INET, SOCK_DGRAM
from struct import unpack, calcsize
import sys

# Listen address
DEFAULT_HOST = "0.0.0.0"

# Reserve a port for UDP protocol
UDP_PORT = 20817

parser = argparse.ArgumentParser(description="Receives position updates via UDP")
parser.add_argument("--plt", action="store_true", help="Plot position updates")
parser.add_argument("--png", type=str, help="Save plot as PNG")
parser.add_argument("--pdf", type=str, help="Save plot as PDF")
parser.add_argument("--addr", default=DEFAULT_HOST, type=str, help="Listen address")
parser.add_argument("--csv", action="store_true", help="Save position updates as CSV")
args = parser.parse_args()

# Create a socket object
s = socket(family=AF_INET, type=SOCK_DGRAM, proto=0)

s.bind((args.addr, UDP_PORT))

# The UDP diagram payload has data fields described in struct format
PAYLOAD_FMT = ">HH5i"
size = calcsize(PAYLOAD_FMT)

timestamps, z1_log, z2_log, z3_log, x_log, y_log = [], [], [], [], [], []
start_time = datetime.now()

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
        real_time = datetime.now()
        sec = timedelta.total_seconds(real_time - start_time)
        timestamps.append(sec)
        z1_log.append(aposz1)
        z2_log.append(aposz2)
        z3_log.append(aposz3)
        x_log.append(lposx)
        y_log.append(lposy)

except KeyboardInterrupt:
    print("\nStopped by user")

# Draw plot on demand
if not (args.plt or args.png or args.pdf or args.csv):
    sys.exit(0)

header = ["Time", "APOSZ1", "APOSZ2", "APOSZ3", "LPOSX", "LPOSY"]

with open("logs.csv", mode="w", encoding="utf8") as csvfile:
    logs_writer = csv.writer(csvfile)
    logs_writer.writerow(header)

    # Each row contains the update timestamp the corresponding stepper positions
    for (t, z1, z2, z3, x, y) in zip(timestamps, z1_log, z2_log, z3_log, x_log, y_log):
        logs_writer.writerow([t, z1, z2, z3, x, y])

# pylint: disable=wrong-import-position
from matplotlib import pyplot as plt

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

ax.plot(timestamps, z1_log, ".-", label="APOSZ1")
ax.plot(timestamps, z2_log, ".-", label="APOSZ2")
ax.plot(timestamps, z3_log, ".-", label="APOSZ3")
ax.plot(timestamps, x_log, ".-", label="LPOSX")
ax.plot(timestamps, y_log, ".-", label="LPOSY")

# Show labels
plt.legend(loc="best")

if args.png:
    plt.savefig(args.png)

if args.pdf:
    plt.savefig(args.pdf)

if args.plt:
    plt.show()
