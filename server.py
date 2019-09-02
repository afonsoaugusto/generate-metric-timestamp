#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
server.py
download SPY data from Yahoo finance and stream it using ZeroMQ
"""

# import libraries
import configparser
import zmq
import time
import numpy as np
from datetime import datetime
import pandas as pd
from influxdb import InfluxDBClient
from random import randrange, uniform


def load_config(section):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[section]


def generate_data(config_data, date):
    start = int(config_data['limit_start'])
    end = int(config_data['limit_end'])

    if end == 0:
        return pd.Series(0, [date])

    data = uniform(start, end)
    return pd.Series([data], [date])


def generate_data_now(config_data):
    index = datetime.today()
    return generate_data(config_data, index)


def convertToTimestamp(data):
    date = data.date[0]
    time = data.time[0]
    now = datetime.combine(date, time)
    return int(datetime.timestamp(now))


def generate_input_influx(row, measurement_name):
    date_now = row.index
    timestamp = convertToTimestamp(date_now)
    return "{measurement} value={value} {timestamp}".format(measurement=measurement_name, value=str(row.values[0]), timestamp=timestamp)


def send_data_influx(row, measurement_name):
    data = []
    data.append(generate_input_influx(row, measurement_name))
    print(data)
    client.write_points(data, database=influx_config['database'],
                        time_precision='s', protocol='line')


if __name__ == '__main__':

    zmq_config = load_config('ZMQ')

    # create the zmq context and socket and bind the socket to port 1234
    socket = zmq.Context(zmq.REP).socket(zmq.PUB)
    socket.bind(zmq_config['connection_server'])

    influx_config = load_config('INFLUXDB')
    client = InfluxDBClient(
        host=influx_config['host'], port=influx_config['port'])
    client.create_database(influx_config['database'])
    measurement_name = influx_config['measurement']

    while True:
        # get row as dataframe
        row = generate_data_now(load_config('DATA'))
        print("----------")

        send_data_influx(row, measurement_name)
        # stream row as python object
        socket.send_pyobj(row)

        # wait 1 second
        time.sleep(1)
