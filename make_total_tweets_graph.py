import datetime
import matplotlib.pyplot as plt

import pdb

def extract_stats(line):
	date,num = line.split(" ",1)
	date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	num = int(num)
	return (date,num)

f = open('data/total_tweets_fixed.txt')
lines = f.readlines()
f.close()

dates = []
nums = []

for line in lines:
	date,num = extract_stats(line)
	dates.append(date)
	nums.append(num)

nums = [i / 1000.0 for i in nums]


ax1 = plt.subplot(111)
ax1.plot_date(dates,nums,'-', color='black')

event1 = ax1.axvline(x=dates[249],linestyle='--',color='red')
event2 = ax1.axvline(x=dates[327],linestyle='--',color='green')
event3 = ax1.axvline(x=dates[381],linestyle='--',color='blue')
event4 = ax1.axvline(x=dates[539],linestyle='--',color='orange')

ax1.legend((event1, event2, event3, event4), ('cop21', 'dicaprio', 'earthday', 'trump-clinton'), prop={'size':10}, loc=2)
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Tweets (Thousands)')
plt.setp(ax1.get_xticklabels(), fontsize=8)
plt.setp(ax1.get_yticklabels(), fontsize=8)

plt.show()

#pdb.set_trace()
'''
axtop = plt.subplot2grid((3,1),(0,0))
ax1 = plt.subplot2grid((3,1),(1,0), rowspan=2)

ax1.axvline(x=dates[249],linestyle='--',color='red')
ax1.axvline(x=dates[327],linestyle='--',color='green')
ax1.axvline(x=dates[381],linestyle='--',color='blue')
ax1.axvline(x=dates[539],linestyle='--',color='orange')

event1 = axtop.axvline(x=dates[249],linestyle='--',color='red')
event2 = axtop.axvline(x=dates[327],linestyle='--',color='green')
event3 = axtop.axvline(x=dates[381],linestyle='--',color='blue')
event4 = axtop.axvline(x=dates[539],linestyle='--',color='orange')

axtop.plot_date(dates,nums,'-', color='black')
ax1.plot_date(dates,nums,'-', color='black')
ax1.set_xlabel('Date')
ax1.text(datetime.date(2015,2,15), 57, 'Number of Tweets (thousands)', rotation='vertical')

axtop.set_autoscale_on(False)
ax1.set_autoscale_on(False)

axtop.axis([dates[0],dates[-1],200,500])
ax1.axis([dates[0],dates[-1],0,200])
axtop.tick_params(axis='x', which='both', bottom='off', labelbottom='off')
ax1.tick_params(axis='x', which='both', top='off')
axtop.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)

ticks = range(250,261,5)
axtop.set_yticks(ticks)
axtop.set_yticklabels(ticks)

ticks = range(0,51,10)
ax1.set_yticks(ticks)
ax1.set_yticklabels(ticks)
plt.setp(ax1.get_xticklabels(), fontsize=8)

axtop.legend((event1, event2, event3, event4), ('cop21', 'dicaprio', 'earthday', 'trump-clinton'), prop={'size':10}, loc=2)

plt.savefig("analysis/total_tweets.eps", format="eps")
plt.show()
'''
