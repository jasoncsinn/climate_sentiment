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

overall_avg_a = sum(avg_as) / len(avg_as)
overall_avg_s = sum(avg_ss) / len(avg_ss)
overall_avg_n = sum(avg_ns) / len(avg_ns)
overall_avg_u = sum(avg_us) / len(avg_us)

pdb.set_trace()

ax1 = plt.subplot(111)
ax1.plot_date(dates,avg_as,'-', color='yellowgreen')
ax1.plot_date(dates,avg_ss,'-', color='lightcoral')
ax1.plot_date(dates,avg_ns,'-', color='lightskyblue')
ax1.plot_date(dates,avg_us,'-', color='gray')
#ax1.plot_date(dates,avg_nus,'-', color='gray')

plt.tight_layout()
plt.setp(ax1.get_xticklabels(), fontsize=8)
plt.savefig("analysis/ambiguity_by_sentiment_combined.png", format="png")
