import sqlite3
from util import parse_tweet, load_lines_from_file
import datetime

import pdb

DB_LOC = 'data/refined_training_data.db'

conn = sqlite3.connect(DB_LOC)
c = conn.cursor()

quit = False

print("For reference: a = activist, s = skeptical, d = unusable, q = quit, other = ignore tweet")
date = raw_input("Enter date to read from (ex: 2015_01_31): ")
fname = "data/full_tweet_data/climate_" + date + ".txt"
start = int(raw_input("Enter tweet # to start from: "))
num_to_read = int(raw_input("Enter # of tweets to read: "))
table = raw_input("Enter table to insert to (training, test, validation): ")
tweets = load_lines_from_file(fname, num_to_read, start)
cur_t = 0
while not quit and cur_t < len(tweets):
	c.execute("SELECT COUNT(*) FROM " + table)
	in_db = c.fetchall()[0][0]
	print("Current number of tweets in " + table + ": " + str(in_db))
	
	date, text, username, location = parse_tweet(tweets[cur_t])
	ui_str = date[4:19] + " - " + username + ": " + text
	print(ui_str)
	inp = raw_input("Tweet #" + str(cur_t + start) + " (a/s/d/q): ")
	to_execute = "INSERT INTO " + table + " VALUES ('"
	to_execute += text + "',"
	if inp == "a":
		to_execute += "'y','a')"
	elif inp == "s":
		to_execute += "'y','s')"
	elif inp == "d":
		to_execute += "'n','n')"
	elif inp == "q":
		quit = True
	if inp == "a" or inp == "s" or inp == "d":
		c.execute(to_execute)
		conn.commit()
		print("Saved.")
	cur_t += 1
c.execute("SELECT COUNT(*) FROM " + table)
in_db = c.fetchall()[0][0]
print("Current number of tweets in " + table + ": " + str(in_db))
conn.close()
print("Connection closed. Exiting.")
