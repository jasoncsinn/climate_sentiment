import datetime
import matplotlib.pyplot as plt
import numpy as np

import pdb

def extract_stats(line):
	date,act,ske = line.split(" ",2)
	date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	act = int(act)
	ske = int(ske)
	return (date,act,ske)

f = open('data/daybyday_tweet_stats_fixed.txt')
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

mu_a = sum(acts)/len(acts)
res_a = [np.float(a) - mu_a for a in acts]

mu_s = sum(skes)/len(skes)
res_s = [np.float(s) - mu_s for s in skes]

fig = plt.figure()

ax1 = fig.add_subplot(211)
ax1.set_autoscale_on(False)
ax1.axis([-0.5,50,-0.2,1])
ax1.acorr(res_a, usevlines=True, maxlags=50, lw=2)
ax1.grid(True)
ax1.axhline(0, color='black', lw=2)
ax1.set_title('Activist Autocorrelations')

ax2 = fig.add_subplot(212, sharex=ax1)
ax2.set_autoscale_on(False)
ax2.axis([-0.5,50,-0.2,1])
ax2.acorr(res_s, usevlines=True, normed=True, maxlags=50, lw=2)
ax2.grid(True)
ax2.axhline(0, color='black', lw=2)
ax2.set_title('Skepticals Autocorrelations')

plt.show()

#fig, ax = plt.subplots()
#ax.plot_date(dates,skes,'-')
#plt.show()
