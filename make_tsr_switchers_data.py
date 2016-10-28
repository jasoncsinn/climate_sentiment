import sqlite3
import pdb
import datetime

from util import get_time_mask,tweet_datetime

class User:
	def __init__(self):
		self.last_date = datetime.datetime(2014,1,1)
		self.pre_sentiment = ''
		self.post_sentiments = {}

linenum = 1
ht = {}

with open('data/tsr_cop21/sentiments_cop21_pre.txt') as f:
	for line in f:
		_, date_str, username, _, sentiment = line.split(" ::---:: ", 4)
		user = ht.get(username, User())
		dt = tweet_datetime(date_str)
		if dt > user.last_date:
			user.last_date = dt
			user.pre_sentiment = sentiment.strip('\n')
		ht[username] = user

		print("Finished parsing line # " + str(linenum) + " username: " + username)
		linenum += 1
#pdb.set_trace()

linenum = 1
with open('data/tsr_cop21/sentiments_cop21_post.txt') as f:
	for line in f:
		_, date_str, username, _, sentiment = line.split(" ::---:: ", 4)
		if username in ht:
			user = ht[username]
			dt = tweet_datetime(date_str)
			user.post_sentiments[dt] = sentiment.strip('\n')
			ht[username] = user

			print("Finished parsing line # " + str(linenum) + " username: " + username)
			linenum += 1
#pdb.set_trace()
with open('data/tsr_cop21/switcher_cop21.txt', 'w') as f:
	for username in ht:
		to_write = username
		user = ht[username]
		to_write += " " + str(user.last_date) + " " + user.pre_sentiment
		sorted_dts = sorted(user.post_sentiments.keys())
		for dt in sorted_dts:
			to_write += " " + user.post_sentiments[dt]
		to_write += "\n"
		f.write(to_write)
		print("Writing username: " + username + " pre sentiment: " + sentiment + " # of post sentiments: " + str(len(sorted_dts)))

