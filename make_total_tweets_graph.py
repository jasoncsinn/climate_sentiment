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


ax = plt.subplot(111)
ax.plot_date(dates,nums,'-')
ax.set_title('Total # of Tweets per day')
ax.set_ylabel('# of Tweets')
ax.set_xlabel('Date')
plt.show()
