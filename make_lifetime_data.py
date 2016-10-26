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

class Tweet:
	def __init__(self):
		self.dates = []
		self.sentiments = []
	def __repr__(self):
		return 'dates: ' + repr(self.dates) + ' sentiments: ' + repr(self.sentiments)

'''
conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()
print("Connected. Querying Unique tweets")
c.execute("SELECT * FROM full_sentiments WHERE NOT text like 'RT%'")
unique_tweets = c.fetchall()
print("Finished Unique tweets. Querying retweets")
c.execute("SELECT * FROM full_sentiments WHERE text like 'RT%' ORDER BY text,date,sentiment")
retweets = c.fetchall()
print("Done")
'''

linenum = 1
with open('data/full_sentiments.txt') as fi:
	ht = {}
	lines = [fi.readline()]
	for line in fi:
		if linenum > 10000000:
			break
		text, date_str, _, _, sentiment = line.split(" ::---:: ", 4)
		sentiment = sentiment.strip()
		if text[0:1] == 'RT':
			text = remove_retweet_prefix(text)
		text = remove_links(text)
		tw = ht.get(text, Tweet())
		tw.dates.append(tweet_date(date_str))
		tw.sentiments.append(sentiment)
		ht[text] = tw
		print("Finished Processing line: " + str(linenum) + " size of ht: " + str(len(ht)))
		linenum += 1
pdb.set_trace()
with open('data/lifetime_data.txt', 'w') as fo:
	for text in ht:
		tw = ht[text]
		tw.dates.sort()
		to_write = text + " ::---:: " + str((tw.dates[-1] - tw.dates[0]).total_seconds())
		to_write += " ::---:: " + str(len(tw.dates))
		to_write += " ::---:: " + " ".join(tw.sentiments) + "\n"
		print(to_write)
		fo.write(to_write)
pdb.set_trace()
'''
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
'''
