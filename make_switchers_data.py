import sqlite3
import pdb
import datetime

from util import get_time_mask

LOC_PRED_DB = 'data/predicted_data.db'
table_names, dates = get_time_mask()

conn = sqlite3.connect(LOC_PRED_DB)
c = conn.cursor()
'''
to_execute = "SELECT username from " + table_names[0] + " GROUP BY username HAVING COUNT(username) > 1"
for i in range(1,len(table_names)):
	to_execute += " UNION "
	to_execute += "SELECT username from " + table_names[i] + " GROUP BY username HAVING COUNT(username) > 1"
c.execute(to_execute)
usernames = c.fetchall()
pdb.set_trace()

full_query = "(SELECT * FROM " + table_names[0] + "WHERE username in (" + to_execute + ")"
for i in range(1,len(table_names)):
	full_query += " UNION "
	full_query += "SELECT * FROM " + table_names[i] + "WHERE username in (" + to_execute + ")"
full_query += ") ORDER BY username,date,sentiment"
c.execute(full_query)
db_tweets = c.fetchall()
'''
c.execute("SELECT * FROM full_sentiments WHERE username in (SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1)) ORDER BY username,date,sentiment")
db_tweets = c.fetchall()
cur_index = 0
ref_index = 0
f = open('data/switcher_data.txt', 'w')
while cur_index < len(db_tweets):
	# slice
	username = db_tweets[ref_index][2]
	sentiments = []
	while db_tweets[cur_index][2] == username and cur_index < len(db_tweets):
		sentiments.append(db_tweets[cur_index][4])
		cur_index += 1
	#pdb.set_trace()
	print(username)
	f.write(username + " " + " ".join(sentiments) + "\n")
	ref_index = cur_index
f.close()
conn.close()
