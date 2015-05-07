# rldw 04/03/15
# https://github.com/rldw
#
# DESCRIPTION:
# - searches all posts on instagram for a given interval in a location
# - plots number of posts per day
# - enter instagram client id below
# - uses Downloader class
#
# USAGE:
# python postsperday.py
# -o --outfile file to save graph to, e.g. pdf or png

import datetime, time, math, argparse
import downloader as dl
import pandas as pd
import matplotlib.pyplot as plt

# add your instagram client id here!
clientid = '69164a0ee9d34973961720101e5956a3'


# parse command line arguments
parser = argparse.ArgumentParser(description='Searches all posts on Instagram for a given interval in a location and plots the number of posts per day')
parser.add_argument('-o','--outfile',
	help='file to save graph to, e.g. pdf or png')
args = parser.parse_args()

# get user input
location  = raw_input("Location: ")
print "Enter in format dd.mm.yyyy or 0 for now"
starttime = raw_input("Start from: ")
endtime   = raw_input("Go to:      ")

# turn input dates to timestamps
if endtime == '0':
	endstamp = int(time.time())
	endtime  = datetime.datetime.fromtimestamp(endstamp).strftime('%d.%m.%Y')
else:
	endstamp = int(time.mktime(datetime.datetime.strptime(endtime, "%d.%m.%Y").timetuple()))

startstamp  = int(time.mktime(datetime.datetime.strptime(starttime, "%d.%m.%Y").timetuple()))

# get timestamps from instagram and store it in posts
client = dl.Downloader(clientid)
client.getGeoCoordinates(location)
posts = client.callAPIuntilTimestamp(startstamp, endstamp)
posts = client.getImageURLsAndTimestamps(posts)


# get posts count per day and store it in a dict
# perday[year][month][day] = post count
perday = {}
for i in range(len(posts)):
	timestamp  = int(posts[i][1])
	datestring = datetime.datetime.fromtimestamp(timestamp)
	y,m,d      = str(datestring).split(' ')[0].split('-')

	if y not in perday:
		perday[y] = {}

	if m not in perday[y]:
		perday[y][m] = [0]*31

	perday[y][m][int(d)-1] += 1


# create a 1D array data where each element is a post count sorted from start
# to end date
# also create labels, also sorted from start to end date in format dd.mm.yyyy
data   = []
labels = []
years  = perday.keys()
years.sort()
for year in years:
	months = perday[year].keys()
	months.sort()
	for month in months:
		for value in perday[year][month]:
			if value > 0:
				day = perday[year][month].index(value) + 1
				data.append(value)

				if day < 10:
					day = "0"+str(day)
				dateasstring = "{0}.{1}.{2}".format(day,month,year)
				labels.append(dateasstring)



plt.style.use('ggplot')
df2 = pd.DataFrame(data)
ax  = df2.plot(alpha=0.6, figsize=(18,6), legend=False, ylim=(0,max(data)*1.05), kind='bar')

# show every nth label, but max 30
n = int(math.ceil(len(data)/30.0))

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks(range(len(labels))[::n])
ax.set_xticklabels(labels[::n], rotation='45')
ax.set_title("Instagram posts in {0} from {1} to {2}".format(location, starttime, endtime))
ax.yaxis.grid(False)
ax.xaxis.grid(True)
ax.set_ylabel('number of posts')

# make bars a little bit bigger
for container in ax.containers:
	plt.setp(container, width=1)

# add some space for labels
plt.subplots_adjust(bottom=0.15)

if args.outfile:
	plt.savefig(args.outfile)
	print "Generated plot and saved it to: " + args.outfile
else:
	plt.show()
