import sqlite3
import pdb

from util import get_time_mask

table_names, dates = get_time_mask()
conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

with open('data/full_sentiments.txt', 'w') as f:
	for t_n in table_names:
		tweets = c.execute("SELECT * FROM " + t_n + " WHERE not sentiment = 'n'")
		print("Done querying table " + t_n)
		to_write = [' ::---:: '.join(t) for t in tweets]
		print("Formatted tweets.")
#		pdb.set_trace()
		f.write("\n".join(to_write))
		print("Written to file. ")
conn.close()
