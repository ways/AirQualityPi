#!/usr/bin/env python3

# sudo pip3 install matplotlib
# sudo pip3 install --upgrade numpy

import matplotlib.pyplot as plt
from datetime import datetime
from csv import reader
import sys

datafile='ccs811_log.csv'
#fileheader='unix,time,co2,tvoc,temp,rpitemp,lat,lon,precision\n'

# TODO: argument to filter on date

x = []
y_co2 = []
y_tvoc = []
y_cpu = []

filterdate = sys.argv[1]

print('Reading file %s.'  % datafile)
with open(datafile, 'r') as file:
  for row_number, row in enumerate(reader(file, delimiter=',')):
  
    if 0 == row_number: # skip header
      continue

    # Filter on date
    if filterdate and row[1].startswith(filterdate):
      pass
    else:
      continue

    # Filter invalid values (have to skip entire row due to pyplot)
    if int(row[2]) < 8000 and int(row[2]) >= 400 and int(row[3]) < 1024:
      pass
    else:
      continue

    x.append(datetime.fromtimestamp(float(row[0])))
    y_co2.append(row[2])
    y_tvoc.append(row[3])
    y_cpu.append(row[5])

    if 0 == row_number%100:
      print ("Processed row", row_number)

f, axarr = plt.subplots(3, sharex=True, num='AirPi')
axarr[0].set_title('CO2 over time')
axarr[0].set_ylabel('CO2 in ppm')
axarr[0].plot(x, y_co2, color='r')
axarr[1].set_title('TVOC over time')
axarr[1].set_ylabel('TVOC in ppb')
axarr[1].plot(x, y_tvoc)
axarr[2].set_title('CPU temp')
axarr[2].set_ylabel('C')
axarr[2].plot(x, y_cpu)

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

#fig = plt.figure() 
#fig.canvas.set_window_title('Airpi') 

plt.show()

