import pdb
import sqlite3

from util import get_time_mask

conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

table_names, dates = get_time_mask()

with open('data/bernie_tweet_data.txt', 'w') as f:
	for t_n in table_names:
		db_tweets = c.execute("SELECT * FROM " + t_n + " WHERE username='BernieSanders'")
		db_tweets = [' ::---:: '.join(x) for x in db_tweets]
		if len(db_tweets) > 0:
			f.write('\n'.join(db_tweets) + '\n')
		print("Done querying " + t_n)
