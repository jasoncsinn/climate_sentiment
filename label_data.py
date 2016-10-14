import sqlite3
from util import parse_tweet, load_lines_from_file
import datetime

import pdb

DB_LOC = 'data/training_data.db'

conn = sqlite3.connect(DB_LOC)
c = conn.cursor()

quit = False

print("For reference: a = activist, s = skeptical, d = unusable, q = quit, other = ignore tweet")
date = raw_input("Enter date to read from (ex: 2015_01_31): ")
fname = "data/full_tweet_data/climate_" + date + ".txt"
start = int(raw_input("Enter tweet # to start from: "))
num_to_read = int(raw_input("Enter # of tweets to read: "))
tweets = load_lines_from_file(fname, num_to_read, start)
cur_t = 0
while not quit and cur_t < len(tweets):
	c.execute("SELECT COUNT(*) FROM tweets")
	in_db = c.fetchall()[0][0]
	print("Current number of tweets in database: " + str(in_db))
	
	date, text, username, location = parse_tweet(tweets[cur_t])
	ui_str = date[4:19] + " - " + username + ": " + text
	print(ui_str)
	inp = raw_input("Tweet #" + str(cur_t + start) + " (a/s/d/q): ")
	to_execute = "INSERT INTO tweets VALUES ('"
	to_execute += text + "','" + date + "','" + username + "','" + location + "','"
	if inp == "a":
		to_execute += "y','a','activist')"
	elif inp == "s":
		to_execute += "y','s','skeptical')"
	elif inp == "d":
		to_execute += "n','n','unusable')"
	elif inp == "q":
		quit = True
	if inp == "a" or inp == "s" or inp == "d":
		c.execute(to_execute)
		conn.commit()
		print("Saved.")
	cur_t += 1
c.execute("SELECT COUNT(*) FROM tweets")
in_db = c.fetchall()[0][0]
print("Current number of tweets in database: " + str(in_db))
conn.close()
print("Connection closed. Exiting.")
