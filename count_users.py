import sqlite3
import pdb

from util import get_time_mask

table_names, dates = get_time_mask()

conn = sqlite3.connect('data/merged_predicted_data.db')
c = conn.cursor()

to_execute = "SELECT username FROM full_tweets GROUP BY username HAVING COUNT(username) > 1"

c.execute(to_execute)

num = 1
with open('data/full_usernames.txt', 'w') as f:
	for row in c:
		username = row[0]
		f.write(username + '\n')
		print(str(num) + ": " + username)
		num += 1
