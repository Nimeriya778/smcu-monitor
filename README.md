SMCU monitor program
====================

The program receives packets from the SMCU model using 
connectionless UDP over IPv4. 
The packet contains new position updates for each simulated
stepper motor full step.

Configuration
-------------

The script is configured via the command line arguments as follows:

```
usage: smcu_monitor.py [-h] [--plt] [--png PNG] [--pdf PDF] [--addr ADDR] [--csv]

optional arguments:
  -h, --help            show this help message and exit
  --plt                 plot position updates
  --png PNG             Save plot as PNG
  --pdf PDF             Save plot as PDF
  --addr ADDR           Listen address
  --csv                 Save position updates as CSV
 
```
