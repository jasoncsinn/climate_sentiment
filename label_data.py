import sqlite3
import util

import pdb

DATA_LOC = 'data/full_tweet_data/climate_2016_07_01.txt'
DB_LOC = 'data/labelled_data.db'

def parse_tweet(tweet_str):
	tweet_str = tweet_str.strip().strip("{").strip("}")
	components = tweet_str.split(":::")
	date = components[0].split(':',1)[1].strip().strip("\"")
	text = components[1].split(':',1)[1].strip().strip("\"").replace("\'", "")
	username = components[3].split(',',1)[0].split(':',1)[1].strip().strip("\"")
	location = components[3].split(',',1)[1].split(':',1)[1].strip().strip("\"").replace("\'","")
	return (date, text, username, location)


conn = sqlite3.connect(DB_LOC)
c = conn.cursor()
tweet_num = int(raw_input("Please enter tweet # to start from: "))
num_tweets = int(raw_input("Please enter # of tweets to read: "))
tweets = util.load_lines_from_file(DATA_LOC, num_tweets, tweet_num)
for tweet_str in tweets:
	date, text, username, location = parse_tweet(tweet_str)
	print(date + " - " + username + ": " + text)
	useful = raw_input("Include tweet? (y/n): ")
	if useful == "y":
		usable = raw_input("Is this tweet usable? (y/n): ")
		final_label = 'unusable'
		sentiment = 'n'
		if usable == "y":
			sentiment = raw_input("What is the sentiment of this tweet? (a/s): ")
			if sentiment == "a":
				final_label = 'activist'
			else:
				final_label = 'skeptical'
		to_execute = "INSERT INTO tweets VALUES (\'" + text + "\',\'" + date + "\',\'" + username + "\',\'" + location + "\',\'" 
		to_execute += usable + "\',\'" + sentiment + "\',\'" + final_label + "\')"
		#print(to_execute)
		c.execute(to_execute)
		conn.commit()
		print("Saved to database.")
conn.close()
print("Connection closed. Exiting.")
