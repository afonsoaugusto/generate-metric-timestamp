#!/usr/bin/env python3

from influxdb import InfluxDBClient
import configparser
import uuid
import random
import datetime
import time
from server import load_config, generate_data, generate_input_influx

config_data = load_config('DATA')
influx_config = load_config('INFLUXDB')
client = InfluxDBClient(host=influx_config['host'], port=influx_config['port'])
client.create_database(influx_config['database'])
measurement_name = influx_config['measurement']

number_of_points = 2500000
numseconds = number_of_points

data = []

base = datetime.datetime.today()
date_list = [base - datetime.timedelta(seconds=x) for x in range(numseconds)]

for date in date_list:
    row = generate_data(config_data, date)
    line = generate_input_influx(row,measurement_name)
    data.append(line)
    print(line)
    print(date)
    print("-----------------------")


client_write_start_time = time.perf_counter()

client.write_points(data, database=influx_config['database'],
                    time_precision='s', batch_size=10000, protocol='line')

client_write_end_time = time.perf_counter()

print("Client Library Write: {time}s".format(
    time=client_write_end_time - client_write_start_time))
