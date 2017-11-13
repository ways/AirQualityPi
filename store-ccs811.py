#!/usr/bin/env python

# sudo pip install smbus2
# sudo pip install Adafruit_CCS811 (doesnt seem to support python3)
# sudo pip install radiocells

from Adafruit_CCS811 import Adafruit_CCS811
from datetime import datetime
from time import sleep, strftime, time
from gpiozero import CPUTemperature
import smbus2
import sys
import os
import csv
import radiocells

datafile='/mnt/ccs811_log.csv'
fileheader='unix,time,co2,tvoc,temp,rpitemp,lat,lon,precision\n'
flushafter=60 # low for debugging
read_timer=5 # in seconds
wifi='wlan0'
verbose = True

# Init sensor
ccs =  Adafruit_CCS811(address=0x5B)

write_count=0
accuracy=False
latlng=[False, False]

# Init data file
with open(datafile, 'a') as file:
  if os.stat(datafile).st_size == 0:
    file.write(fileheader)

  # Init cvs
  csvwriter = csv.writer(file, delimiter=',')
  if verbose: print('Writing to file %s with header: %s' % (datafile, fileheader))

  # Attempt to get posision
  accuracy, latlng = radiocells.locate(device=wifi)

  # Main loop
  while True:
    try:

      if ccs.available():
        temp = ccs.calculateTemperature()
        if not ccs.readData():
          datarow=[time(), datetime.now(), ccs.geteCO2(), ccs.getTVOC(), ccs.calculateTemperature(), CPUTemperature().temperature, latlng[0], latlng[1], accuracy]
          if verbose: print(datarow)
          csvwriter.writerow(datarow)
          write_count+=1

          # Flush to disk after some time
          if flushafter < write_count:
            print('Flushing to disk')
            file.flush()

            # Update posision while we're at it
            accuracy, latlng = radiocells.locate(device=wifi)

            write_count=0
        else:
          print("Error waiting for sensor.")
      else:
        print ("Error opening sensor")

    except IOError() as e:
      print("Error reading CCS881 or writing file", e)

    sleep(read_timer)

