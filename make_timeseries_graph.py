import datetime
import matplotlib.pyplot as plt

import pdb

def extract_stats(line):
	date,act,ske = line.split(" ",2)
	date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	act = int(act)
	ske = int(ske)
	return (date,act,ske)

f = open('analysis/daybyday_tweet_stats_fixed.txt')
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

fig, ax = plt.subplots()
ax.plot_date(dates,skes,'-')
plt.show()
