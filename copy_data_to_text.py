import sqlite3
import pdb
import datetime

from util import get_time_mask, tweet_datetime

table_names, dates = get_time_mask()
conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

start_dt = datetime.datetime(2016,9,27,0,0,0)
end_dt = datetime.datetime(2016,10,7,0,0,0)

#with open ('data/sentiments_dicaprio.txt', 'w') as f:
with open ('data/tsr_trump/post_data.txt', 'w') as f:
	for t_n in table_names[75:83]:
#		tweets = c.execute("SELECT * FROM " + t_n + " WHERE not sentiment = 'n'")
		c.execute("SELECT * FROM " + t_n)
		tweets = c.fetchall()
		print("Done querying table " + t_n)
		to_write = []
		tweets = tweets
		for t in tweets:
			dt = tweet_datetime(t[1])
			if dt > start_dt and dt < end_dt:
				to_write.append(' ::---:: '.join(t))
		f.write("\n".join(to_write))
		print("Written to file.")

'''
with open('data/full_sentiments.txt', 'w') as f:
	for t_n in table_names:
		tweets = c.execute("SELECT * FROM " + t_n + " WHERE not sentiment = 'n'")
		print("Done querying table " + t_n)
		to_write = [' ::---:: '.join(t) for t in tweets]
		print("Formatted tweets.")
#		pdb.set_trace()
		f.write("\n".join(to_write))
		print("Written to file. ")
'''
conn.close()
