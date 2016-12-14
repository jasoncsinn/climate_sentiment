import datetime
import sqlite3

from util import get_time_mask, tweet_datetime

table_names, dates = get_time_mask()
conn = sqlite3.connect('data/discrete_predicted_data.db')
c = conn.cursor()

event_names = ['cop21', 'dicaprio', 'earthday','trump']
dates = [[datetime.datetime(2015,12,2,0,0,0),
		datetime.datetime(2015,12,12,0,0,0),	
		datetime.datetime(2015,12,22,0,0,0)],
	[datetime.datetime(2016,2,18,0,0,0),
		datetime.datetime(2016,2,28,0,0,0),
		datetime.datetime(2016,3,9,0,0,0)],
	[datetime.datetime(2016,4,12,0,0,0),
		datetime.datetime(2016,4,22,0,0,0),
		datetime.datetime(2016,5,1,0,0,0)],
	[datetime.datetime(2016,9,17,0,0,0),
		datetime.datetime(2016,9,27,0,0,0),
		datetime.datetime(2016,10,7,0,0,0)]]
table_names = [[34,42],[45,55],[54,61],[75,83]]

t_ns, ds = get_time_mask()

for i,event in enumerate(event_names):
	pre_start = dates[i][0]
	event_d = dates[i][1]
	post_end = dates[i][2]
	start_table = table_names[i][0]
	end_table = table_names[i][1]
	with open('data/tsr_' + event + '/pre_disc_data.txt', 'w') as f:
		for t_n in t_ns[start_table:end_table]:
			c.execute("SELECT * FROM " + t_n)
			tweets = c.fetchall()
			print("Done querying table " + t_n)
			to_write = []
			for t in tweets:
				dt = tweet_datetime(t[1])
				if dt > pre_start and dt < event_d:
					to_write.append(' ::---:: '.join(t))
			f.write("\n".join(to_write))
			print("Written to file.")
	with open('data/tsr_' + event + '/post_disc_data.txt', 'w') as f:
		for t_n in t_ns[start_table:end_table]:
			c.execute("SELECT * FROM " + t_n)
			tweets = c.fetchall()
			print("Done querying table " + t_n)
			to_write = []
			for t in tweets:
				dt = tweet_datetime(t[1])
				if dt > event_d and dt < post_end:
					to_write.append(' ::---:: '.join(t))
			f.write("\n".join(to_write))
			print("Written to file.")
