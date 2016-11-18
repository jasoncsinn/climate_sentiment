import datetime
import matplotlib.pyplot as plt

import pdb

def extract_stats(line):
	date,act,ske = line.split(" ",2)
	date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	act = int(act)
	ske = int(ske)
	return (date,act,ske)

f = open('data/timeseries_data_fixed.txt')
lines = f.readlines()
f.close()

dates = []
acts = []
skes = []

for line in lines:
	date,act,ske = extract_stats(line)
	dates.append(date)
	acts.append(act)
	skes.append(ske)

ax1 = plt.subplot(111)
#ax2 = plt.subplot(212)
ax1.plot_date(dates,skes,'-')
ax1.set_ylabel('Number of Tweets')
ax1.set_xlabel('Date')
ax1.set_ylim([0,160000])

plt.tight_layout()
plt.setp(ax1.get_xticklabels(), fontsize=8)
#ax2.plot_date(dates,skes,'-')
#ax2.set_title('Skepticals Timeseries Graph')
#ax2.set_ylabel('# of Tweets')
#ax2.set_xlabel('Date')
plt.savefig('analysis/ts_s.eps', format='eps')
#plt.show()
