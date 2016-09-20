import sqlite3
import pdb
import datetime

LOC_PRED_DB = 'data/predicted_data.db'

conn = sqlite3.connect(LOC_PRED_DB)
c = conn.cursor()
c.execute("SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1)")
usernames = c.fetchall()
pdb.set_trace()

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
