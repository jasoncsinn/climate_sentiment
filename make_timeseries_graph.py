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

ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
ax1.plot_date(dates,acts,'-')
ax1.set_title('Activists Timeseries Graph')
ax2.plot_date(dates,skes,'-')
ax2.set_title('Skepticals Timeseries Graph')
plt.show()
