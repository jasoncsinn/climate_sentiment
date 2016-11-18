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


ax1 = plt.subplot(111)

ax1.plot_date(dates,nums,'-')
ax1.set_ylabel('Number of Tweets')
ax1.set_xlabel('Date')


plt.tight_layout()
plt.setp(ax1.get_xticklabels(), fontsize=8)
plt.savefig("analysis/total_tweets.eps", format="eps")
#plt.show()
