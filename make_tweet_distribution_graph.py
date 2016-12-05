import pdb
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime

def tweet_date(s):
	return datetime.datetime.strptime(s,'%Y-%m-%d').date()

def extract_sentiment_stats(line):
	date,act,ske = line.split(" ",2)
	date = tweet_date(date)
	act = int(act)
	ske = int(ske)
	return (date, act, ske)

def extract_total_tweet_stats(line):
	date, num = line.split(" ", 1)
	date = tweet_date(date)
	num = int(num)
	return (date, num)

with open('data/total_tweets_fixed.txt') as f:
	tt_lines = f.readlines()

dates = []
total_tweets = []
for line in tt_lines:
	date,num = extract_total_tweet_stats(line)
	dates.append(date)
	total_tweets.append(num)

with open('data/timeseries_data_fixed.txt') as f:
	ts_lines = f.readlines()

acts = []
skes = []
for line in ts_lines:
	_,act,ske = extract_sentiment_stats(line)
	acts.append(act)
	skes.append(ske)
#pdb.set_trace()

# Normalize
acts = [100.0 * acts[i] / total_tweets[i] for i in range(len(dates))]
skes = [100.0 * skes[i] / total_tweets[i] for i in range(len(dates))]

acts = [acts[i] + skes[i] for i in range(len(dates))]

ax = plt.subplot(111)
ax.fill_between(dates, 0, skes, facecolor='lightcoral', linewidth=0)
ax.fill_between(dates, skes, acts, facecolor='yellowgreen', linewidth=0)
ax.fill_between(dates, acts, 100, facecolor='lightskyblue', linewidth=0)
legend_red = mpatches.Patch(color='lightcoral', label='Skeptics')
legend_green = mpatches.Patch(color='yellowgreen', label='Activists')
legend_blue = mpatches.Patch(color='lightskyblue', label='Other')
ax.legend(handles=[legend_red, legend_green, legend_blue])
ax.set_ylabel('Percent of tweets')
ax.set_xlabel('Date')

plt.setp(ax.get_xticklabels(), fontsize=8)

plt.savefig("analysis/tweet_distribution.png", format="png")
plt.show()
