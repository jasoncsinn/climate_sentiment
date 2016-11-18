import sqlite3
import pdb
import datetime

from util import get_time_mask

def tweet_date(db_tweet):
	return datetime.datetime.strptime(db_tweet[1],'%a %b %d %H:%M:%S +0000 %Y').date()

table_names, dates = get_time_mask()

conn = sqlite3.connect('data/refined_predicted_data.db')
c = conn.cursor()
delta = datetime.timedelta(1)

f =open('data/timeseries_data.txt', 'w')
for i in range(len(table_names)):
	cur_date = dates[i]
	end_date = dates[i+1]
	c.execute(" SELECT * FROM " + table_names[i] + " WHERE NOT sentiment='n'")
	db_tweets = c.fetchall()
	date_mask = []
	while cur_date <= end_date:
		date_mask.append(cur_date)
		cur_date += delta

	for i in range(len(date_mask)):
		tweets = [t for t in db_tweets if tweet_date(t) == date_mask[i]]
		a_t = len([t for t in tweets if t[4] == 'a'])
		s_t = len([t for t in tweets if t[4] == 's'])
		string = "Day: " + str(date_mask[i]) + " Activists: " + str(a_t) + " Skepticals: " + str(s_t)
		f.write(str(date_mask[i]) + " " + str(a_t) + " " + str(s_t) + "\n")
		print(string)
f.close()
conn.close()
