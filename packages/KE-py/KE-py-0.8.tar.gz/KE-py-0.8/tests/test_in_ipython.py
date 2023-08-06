# coding=u8
import logging
from KE import KE
import csv
import time
import queue
import configparser
from datetime import datetime, timedelta
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

client = KE(host='solution-1', port=7033, username='admin', password='KYLIN', version=3)
projects = client.projects()
print(projects)

cube = client.cubes('kylin_sales_cube')[0]

start = datetime(2019, 1, 1, 8, 0)
end = datetime(2019, 1, 31, 8, 0)

segments = cube.segments(start_time=start, end_time=end)
seg_list = segments.list_segments()
s0 = segments.list_segments()[0]
