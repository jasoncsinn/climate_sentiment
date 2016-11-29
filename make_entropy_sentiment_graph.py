import datetime
import matplotlib.pyplot as plt
import pdb

def extract_stats(line):
#	pdb.set_trace()
	date, avg_a, avg_s, avg_n, avg_u, avg_nu = line.split(" ", 5)
	date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	avg_a = float(avg_a)
	avg_s = float(avg_s)
	avg_n = float(avg_n)
	avg_u = float(avg_u)
	avg_nu = float(avg_nu)

	return (date, avg_a, avg_s, avg_n, avg_u, avg_nu)

f = open('data/ambiguity_sentiment_fixed.txt')
lines = f.readlines()
f.close()

dates = []
avg_as = []
avg_ss = []
avg_ns = []
avg_us = []
avg_nus = []

for line in lines:
	date, avg_a, avg_s, avg_n, avg_u, avg_nu = extract_stats(line)
	dates.append(date)
	avg_as.append(avg_a)
	avg_ss.append(avg_s)
	avg_ns.append(avg_n)
	avg_us.append(avg_u)
	avg_nus.append(avg_nu)


ax1 = plt.subplot(111)
ax1.plot_date(dates,avg_as,'-', color='blue')
ax1.plot_date(dates,avg_ss,'-', color='red')
ax1.plot_date(dates,avg_ns,'-', color='gray')
ax1.plot_date(dates,avg_us,'-', color='black')
ax1.plot_date(dates,avg_nus,'-', color='green')

plt.tight_layout()
plt.setp(ax1.get_xticklabels(), fontsize=8)
plt.savefig("analysis/ambiguity_by_sentiment.eps", format="eps")
