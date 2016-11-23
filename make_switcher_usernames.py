import sqlite3
import pdb

from util import get_time_mask

table_names,_ = get_time_mask()

conn = sqlite3.connect('data/refined_predicted_data.db')
c = conn.cursor()

c.execute("SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1)")
usernames = c.fetchall()

pdb.set_trace()

with open('data/switchers/switcher_usernames.txt', 'w') as f:
	for username in usernames:
		f.write(username[0] + "\n")
