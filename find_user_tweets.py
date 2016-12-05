import pdb
import sqlite3

from util import get_time_mask

user_ht = {}
with open('data/full_usernames.txt') as f:
	usernames = f.readlines()
	usernames = [un.strip('\n') for un in usernames]

for un in usernames:
	user_ht[un] = un + ":"

table_names, dates = get_time_mask()
conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

for table_name in table_names:
	c.execute("SELECT * FROM " + table_name)
	for row in c:
		_,_,un,_,sent,ent = row
		if un in user_ht:
			user_ht[un] = user_ht[un] + " " + sent + " " + ent
		print(table_name + " username: " + un + " sent: " + sent + " ent: " + ent)

with open('data/ent_data.txt', 'w') as f:
	for un in user_ht:
		f.write(user_ht[un] + '\n')

pdb.set_trace()

'''
conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

table_names, dates = get_time_mask()

with open('data/hmm/obama_full_tweet_data.txt', 'w') as f:
	for t_n in table_names:
		db_tweets = c.execute("SELECT * FROM " + t_n + " WHERE text like '%obama%'")
		db_tweets = [' ::---:: '.join(x) for x in db_tweets]
		if len(db_tweets) > 0:
			f.write('\n'.join(db_tweets) + '\n')
		print("Done querying " + t_n)
'''
