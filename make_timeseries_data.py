import sqlite3
import pdb
import datetime

class Tweet():
	def __init__(self, text, date, username, location, sentiment):
		self.text = text
		self.date = date
		self.username = username
		self.location = location
		self.sentiment = sentiment

def tweet_date(db_tweet):
	return datetime.datetime.strptime(db_tweet[1],'%a %b %d %H:%M:%S +0000 %Y').date()

LOC_PRED_DB = 'data/predicted_data.db'

conn = sqlite3.connect(LOC_PRED_DB)
c = conn.cursor()
#c.execute("SELECT * FROM full_sentiments")
#c.execute("SELECT * FROM full_sentiments WHERE username in (SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1)) ORDER BY date")
c.execute("SELECT * FROM climate_2016_04_29 WHERE NOT sentiment='n'")

db_tweets = c.fetchall()
dt_format = '%a %b %d %H:%M:%S +0000 %Y'
cur_date = datetime.date(2016,4,22)
end_date = datetime.date(2016,4,29)
delta = datetime.timedelta(1)
date_mask = []
#activist_tweets = []
#skeptical_tweets = []
f = open('data/daybyday_tweet_stats_2016.txt', 'a')

while cur_date <= end_date:
	date_mask.append(cur_date)
	cur_date += delta
for i in range(len(date_mask)):
	tweets = [t for t in db_tweets if tweet_date(t) == date_mask[i]]
	a_t = len([t for t in tweets if t[4] == 'a'])
	s_t = len([t for t in tweets if t[4] == 's'])
	#activist_tweets.append(a_t)
	#skeptical_tweets.append(s_t)
	string = "Day: " + str(date_mask[i]) + " Activists: " + str(a_t) + " Skepticals: " + str(s_t)
	f.write(str(date_mask[i]) + " " + str(a_t) + " " + str(s_t) + "\n")
	print(string)
f.close()
#pdb.set_trace()
'''
while cur_date <= end_date:
	# Find all tweets on the current date
	cur_tweet_date = tweet_date(db_tweets[cur_index])
	ref_index = cur_index
	while cur_tweet_date == cur_date:
		cur_index += 1
		cur_tweet_date = tweet_date(db_tweets[cur_index])
	real_tweets = [t for t in db_tweets if tweet_date(t) == cur_date]
	pdb.set_trace()
	cur_date += delta
'''
'''
tweets = []
for row in db_tweets:
	tweets.append(Tweet(row[0],row[1],row[2],row[3],row[4]))
stoa = []
atos = []
c.execute("SELECT username FROM sentiments GROUP BY username HAVING (COUNT(username) > 1)")
usernames = c.fetchall()
for username in usernames:
	#pdb.set_trace()
	user_tweets = [t for t in tweets if t.username == username[0]]
	print(username[0] + " Num Tweets: " + str(len(user_tweets)))
	first_sentiment = user_tweets[0].sentiment
	for user_tweet in user_tweets:
		if user_tweet.sentiment != first_sentiment and first_sentiment == 's':
			stoa.append(username[0])
		elif user_tweet.sentiment != first_sentiment and first_sentiment == 'a':
			atos.append(username[0])
pdb.set_trace()
'''

