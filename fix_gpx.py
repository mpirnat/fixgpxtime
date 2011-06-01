import datetime
import re
from dateutil.relativedelta import relativedelta

offset = relativedelta(hours=4)
timestamp_pattern = re.compile('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
time_format = '%Y-%m-%dT%H:%M:%SZ'

f = open('RK_gpx _2011-05-29_1024AM.gpx', 'r')
data = f.readlines()
f.close()

data_out = []
for line in data:
    match = timestamp_pattern.search(line)
    if not match:
        data_out.append(line)
        continue
    timestamp_in = match.group()
    date_in = datetime.datetime.strptime(match.group(), time_format)
    date_out = date_in + offset
    timestamp_out = date_out.strftime(time_format)
    line = line.replace(timestamp_in, timestamp_out)
    data_out.append(line)

f = open("fixed.gpx", 'w')
f.writelines(data_out)
f.close()

