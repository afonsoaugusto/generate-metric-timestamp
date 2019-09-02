#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
client.py
listens on ZeroMQ's port and plot every new data point
"""

# import libraries
import zmq
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import configparser

register_matplotlib_converters()

config = configparser.ConfigParser()
config.read('config.ini')
zmq_config = config['ZMQ']

# create the zmq client and listen on port 1234
socket = zmq.Context(zmq.REP).socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, '')
socket.connect(zmq_config['connection_client'])

# create an empty dataframe that will store streaming data
df = pd.DataFrame()

# create plot
plt.ion()  # <-- work in "interactive mode"
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.30, bottom=0.15)
fig.canvas.set_window_title('Live Chart')
ax.set_title("Data Simulate")

axcolor = 'lightgoldenrodyellow'
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    print("----------HHHHHH----------")


button.on_clicked(reset)

axstart = plt.axes([0.025, 0.5, 0.20, 0.05], facecolor=axcolor)
axend = plt.axes([0.025, 0.4, 0.20, 0.06], facecolor=axcolor)

init_start = int(config['DATA']['limit_start'])
init_end = int(config['DATA']['limit_end'])
sfreq = Slider(axstart, 'Start', 0, 3000, valinit=init_start, valstep=1, valfmt='%1.0f')
samp = Slider(axend, 'End', 0, 3000, valinit=init_end, valstep=1, valfmt='%1.0f')

def update(position,val):
    config_data = config['DATA']
    config_data[position]=str(int(val))

    with open('config.ini', 'w+') as configfile:
        config.write(configfile)

def update_start(val):
    update('limit_start',val)

def update_end(val):    
    update('limit_end',val)

sfreq.on_changed(update_start)
samp.on_changed(update_end)

# act on new data coming from streamer
while True:
    # receive python object
    row = socket.recv_pyobj()

    # append new row to dataframe
    df = pd.concat([df, row])

    # plot all data
    ax.plot(df, color='r')
    ax.set_title("Data Simulate "+str(row.values))

    # show the plot
    plt.show()
    plt.pause(0.0001)  # <-- sets the current plot until refreshed

    # be nice to the cpu :)
    time.sleep(.1)

