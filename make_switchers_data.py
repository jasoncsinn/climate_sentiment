import sqlite3
import pdb
import datetime

from util import get_time_mask,tweet_datetime

user_ht = {}
with open('data/switcher_usernames.txt') as f:
	for un in f:
		un = un.strip()
		user_ht[un] = {}
linenum = 1
#with open('data/full_sentiments.txt') as f:
#with open('data/sentiments_dicaprio.txt') as f:
with open('data/switchers/sentiments_bn_khaled.txt') as f:
	for line in f:
		_, date_str, username, _, sentiment = line.split(" ::---:: ", 4)
#		pdb.set_trace()
		if username in user_ht:
			
			dt = tweet_datetime(date_str)
			dt_s_ht = user_ht[username]
			dt_s_ht[dt] = sentiment.strip()
			user_ht[username] = dt_s_ht
		print("Finished parsing line # " + str(linenum) + " username: " + username)
		linenum += 1
#pdb.set_trace()
#with open ('data/switcher_data.txt', 'w') as f:
#with open('data/switcher_dicaprio.txt', 'w') as f:
with open('data/switchers/switcher_bn_khaled.txt', 'w') as f:
	for username in user_ht:
		to_write = username
		dt_s_ht = user_ht[username]
		sorted_dts = sorted(dt_s_ht.keys())
		for dt in sorted_dts:
			to_write += " " + dt_s_ht[dt]
		to_write += "\n"
		f.write(to_write)
		print("Writing username: " + username + " # sentiments: " + str(len(sorted_dts)))

#conn = sqlite3.connect(LOC_PRED_DB)
#c = conn.cursor()
'''
username = '0001Angel'
to_execute = "SELECT * from " + table_names[0] + " WHERE username='" + username + "'"
for i in range(1,len(table_names)):
	to_execute += " UNION "
	to_execute += "SELECT * from " + table_names[i] + " WHERE username='" + username + "'"
c.execute(to_execute)
tweets = c.fetchall()
pdb.set_trace()
full_query = "(SELECT * FROM " + table_names[0] + "WHERE username in (" + to_execute + ")"
for i in range(1,len(table_names)):
	full_query += " UNION "
	full_query += "SELECT * FROM " + table_names[i] + "WHERE username in (" + to_execute + ")"
full_query += ") ORDER BY username,date,sentiment"
c.execute(full_query)
db_tweets = c.fetchall()
#c.execute("SELECT * FROM full_sentiments WHERE username in (SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1)) ORDER BY username,date,sentiment")
c.execute("SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1)")
usernames = c.fetchall()
print(str(len(usernames)))
f = open('data/switcher_usernames.txt', 'w')
for t in usernames:
	f.write(t[0] + "\n")
f.close()
conn.close()
'''


'''
f = open('data/switcher_usernames.txt', 'r')
usernames = f.readlines()
f.close()

usernames = set(usernames)

c.execute("SELECT * FROM full_sentiments ORDER BY username")
db_tweets = c.fetchall()
cur_index = 0
ref_index = 0
f = open('data/switcher_data.txt', 'w')
while cur_index < len(db_tweets):
	# slice
	username = db_tweets[ref_index][2]
	if username in usernames:
		sentiments = []
		while db_tweets[cur_index][2] == username and cur_index < len(db_tweets):
			sentiments.append((db_tweets[cur_index][4], tweet_datetime(db_tweets[cur_index][1])))
			cur_index += 1
		sorted(sentiments, key=lambda x: x[1]) 
		print(username)
		sentiment_str = " "
		for s in sentiments:
			sentiment_str += s[0] + " "
		sentiment_str += "\n"
		print(sentiment_str)
		pdb.set_trace()
		f.write(username + " " + " ".join(sentiments) + "\n")
	else:
		while db_tweets[cur_index][2] == username and cur_index <len(db_tweets):
			cur_index += 1
		print("not " + username)
	ref_index = cur_index
f.close()
conn.close()
'''
