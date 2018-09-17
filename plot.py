import datetime
import dateutil.parser
import sys
import boto3
from boto3.dynamodb.conditions import Key, Attr
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

# Get time range (double the given hours to compare last cycle)

hours = 24
if len(sys.argv) > 1:
    now = dateutil.parser.parse(sys.argv[1])
else:
    now = datetime.datetime.now()
end_t = int(now.timestamp())
start_t = end_t - 60 * 60 * hours * 2
half_t = (start_t + end_t) / 2

# Get data from DynamoDB

dynamo = boto3.resource('dynamodb')
table = dynamo.Table('upordown-history')

response = table.query(
    KeyConditionExpression=Key('product').eq('BTC-USD') & Key('t').between(start_t * 1000, end_t * 1000)
)

# Build lines from data
# ------------------------------------------------------------------------------

x1 = []
y1 = []
x2 = []
y2 = []

for i in response['Items']:
    t = int(i['t'])/1000
    d = datetime.datetime.fromtimestamp(t)
    if t < half_t:
        x1.append(d)
        y1.append(float(i['price']))
    else:
        x2.append(d)
        y2.append(float(i['price']))

# Connect the lines
x1.append(x2[0])
y1.append(y2[0])

# Color the lines
if y2[-1] > y2[0]:
    upordown = 'up'
    upordown_color = 'green'
else:
    upordown = 'down'
    upordown_color = 'red'

change = abs(y2[0] - y2[-1])
current = y2[-1]

# Build and format graph
# ------------------------------------------------------------------------------

rcParams['font.sans-serif'] = ['Droid Sans Mono']
rcParams.update({'font.weight': 'normal'})
rcParams.update({'xtick.labelsize': 8})
rcParams.update({'ytick.labelsize': 8})

fig, axs = plt.subplots(1, 1)
fig.set_size_inches(6, 2)

axs.plot(x1, y1, color='#cccccc')
axs.plot(x2, y2, color=upordown_color)
axs.yaxis.tick_right()
axs.plot(x2[-1], y2[-1], marker='o', color=upordown_color)

axs.spines['top'].set_visible(False)
axs.spines['bottom'].set_visible(False)
axs.spines['left'].set_visible(False)
axs.spines['right'].set_visible(False)

plt.gcf().autofmt_xdate()
date_format = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(date_format)

plt.tight_layout()

# Save image

filename = 'graphs/%s-%dh.png' % (now.strftime('%Y%m%d-%H%M%S'), hours)
plt.savefig(filename)

# Upload to S3

bucketname = 'upordown-graphs'
s3 = boto3.resource('s3')
data = open(filename, 'rb')
uploaded = s3.Bucket(bucketname).put_object(Key=filename, Body=data, ACL='public-read', ContentType='image/png')
filename = 'https://s3.amazonaws.com/%s/%s' % (bucketname, filename)

title = 'BTC has gone %s $%.2f to $%.2f in the last %d hours' % (upordown, change, current, hours)

print(filename)
print(title)
