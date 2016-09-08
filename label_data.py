import sqlite3
import util

import pdb

DATA_LOC = 'data/full_tweet_data/climate_2016_04_01.txt'
DB_LOC = 'data/labelled_data.db'

def parse_tweet(tweet_str):
	tweet_str = tweet_str.strip().strip("{").strip("}")
	components = tweet_str.split(":::")
	date = components[0].split(':')[1].strip().strip("\"")
	text = components[1].split(':',1)[1].strip().strip("\"").replace("\'", "")
	username = components[3].split(',',1)[0].split(':',1)[1].strip().strip("\"")
	location = components[3].split(',',1)[1].split(':',1)[1].strip().strip("\"")
	return (date, text, username, location)


conn = sqlite3.connect(DB_LOC)
c = conn.cursor()
tweet_num = int(raw_input("Please enter tweet # to start from: "))
num_tweets = int(raw_input("Please enter # of tweets to read: "))
tweets = util.load_lines_from_file(DATA_LOC, num_tweets, tweet_num)
for tweet_str in tweets:
	date, text, username, location = parse_tweet(tweet_str)
	print(date + " - " + username + ": " + text)
	useful = raw_input("Is this tweet useful? (y/n): ")
	if useful == "y":
		subjective = raw_input("Is this tweet subjective? (y/n): ")
		sentiment = 'n'
		if subjective == "y":
			sentiment = raw_input("What is the sentiment of this tweet? (a/s): ")
		to_execute = "INSERT INTO tweets VALUES (\'" + text + "\',\'" + date + "\',\'" + username + "\',\'" + location + "\',\'" + subjective + "\',\'" + sentiment + "\')"
		print(to_execute)
		c.execute(to_execute)
		print("Saved to database.")
conn.commit()
print("Commited to database. Closing connection.")
conn.close()
print("Connection closed. Exiting.")
