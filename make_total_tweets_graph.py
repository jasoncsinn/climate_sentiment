import datetime
import matplotlib.pyplot as plt

import pdb

def extract_stats(line):
	date,num = line.split(" ",1)
	date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	num = int(num)
	return (date,num)

f = open('data/total_tweets_2016_fixed.txt')
lines = f.readlines()
f.close()

dates = []
nums = []

for line in lines:
	date,num = extract_stats(line)
	dates.append(date)
	nums.append(num)

fig, ax = plt.subplots()
ax.plot_date(dates,nums,'-')
plt.show()
