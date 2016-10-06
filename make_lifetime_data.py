import sqlite3
import pdb
import datetime

def remove_retweet_prefix(tweet_text):
	tweet_tokens = tweet_text.split()[2:]
	return " ".join(tweet_tokens)

def remove_links(tweet_text):
	tweet_tokens = tweet_text.split()
	tweet_tokens = filter(lambda x: "https:\\/\\/t.co\\/" not in x, tweet_tokens)
	return " ".join(tweet_tokens)

def tweet_date(date_text):
        return datetime.datetime.strptime(date_text,'%a %b %d %H:%M:%S +0000 %Y')

conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()
c.execute("SELECT * FROM full_sentiments WHERE NOT text like 'RT%'")
unique_tweets = c.fetchall()
c.execute("SELECT * FROM full_sentiments WHERE text like 'RT%' ORDER BY text,date,sentiment")
retweets = c.fetchall()

ut_ht = {}
for t in unique_tweets:
	text = remove_links(t[0])
	l = ut_ht.get(text, [])
	l.append((tweet_date(t[1]),t[4]))
	ut_ht[text] = l

rt_ht = {}
for t in retweets:
	text = remove_retweet_prefix(t[0])
	text = remove_links(text)
	l = rt_ht.get(text, [])
	l.append((tweet_date(t[1]),t[4]))
	rt_ht[text] = l

#pdb.set_trace()

intersection = set(ut_ht.keys()) & set(rt_ht.keys())
f = open('data/lifetime_data.txt', 'w')
for t in intersection:
	intersect = ut_ht[t]
	intersect.extend(rt_ht[t])
	dates,sentiments = zip(*intersect)
	dates = list(dates)
	dates.sort()
	to_write = t + " ::---:: " + str((dates[-1] - dates[0]).total_seconds()) + " ::---:: " + str(len(dates)) + " ::---:: " + " ".join(sentiments) + "\n"
	f.write(to_write)
f.close()
