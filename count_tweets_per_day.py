import sqlite3
import pdb
import datetime

def tweet_date(db_tweet):
	return datetime.datetime.strptime(db_tweet[1],'%a %b %d %H:%M:%S +0000 %Y').date()

table_names = ['climate_2016_01_01','climate_2016_01_08','climate_2016_01_15','climate_2016_01_22','climate_2016_01_29','climate_2016_02_05','climate_2016_02_12','climate_2016_02_19','climate_2016_02_26','climate_2016_03_04','climate_2016_03_11','climate_2016_03_18','climate_2016_03_25','climate_2016_04_01','climate_2016_04_08','climate_2016_04_15','climate_2016_04_22','climate_2016_04_29','climate_2016_05_06','climate_2016_05_13','climate_2016_05_20','climate_2016_05_27','climate_2016_06_03','climate_2016_06_10','climate_2016_06_17','climate_2016_06_24','climate_2016_07_01','climate_2016_07_08','climate_2016_07_15','climate_2016_07_22','climate_2016_07_29','climate_2016_08_05','climate_2016_08_12','climate_2016_08_19']
dates = [datetime.date(2015,12,25),datetime.date(2016,1,1),datetime.date(2016,1,8),datetime.date(2016,1,15),datetime.date(2016,1,22),datetime.date(2016,1,29),datetime.date(2016,2,5),datetime.date(2016,2,12),datetime.date(2016,2,19),datetime.date(2016,2,26),datetime.date(2016,3,4),datetime.date(2016,3,11),datetime.date(2016,3,18),datetime.date(2016,3,25),datetime.date(2016,4,1),datetime.date(2016,4,8),datetime.date(2016,4,15),datetime.date(2016,4,22),datetime.date(2016,4,29),datetime.date(2016,5,6),datetime.date(2016,5,13),datetime.date(2016,5,20),datetime.date(2016,5,27),datetime.date(2016,6,3),datetime.date(2016,6,10),datetime.date(2016,6,17),datetime.date(2016,6,24),datetime.date(2016,7,1),datetime.date(2016,7,8),datetime.date(2016,7,15),datetime.date(2016,7,22),datetime.date(2016,7,29),datetime.date(2016,8,5),datetime.date(2016,8,12),datetime.date(2016,6,19)]

conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()
delta = datetime.timedelta(1)

f = open('data/total_tweets_2016.txt', 'a')
for i in range(len(table_names)):
	cur_date = dates[i]
	end_date = dates[i+1]
	c.execute("SELECT * FROM " + table_names[i])
#cur_date = datetime.date(2016,8,12)
#end_date = datetime.date(2016,8,19)
#c.execute("SELECT * FROM climate_2016_08_19")
	db_tweets = c.fetchall()
	date_mask = []
	while cur_date <= end_date:
		date_mask.append(cur_date)
		cur_date += delta

	for i in range(len(date_mask)):
		tweets = [t for t in db_tweets if tweet_date(t) == date_mask[i]]
		string = "Day: " + str(date_mask[i]) + " Num: " + str(len(tweets))
		print(string)
		f.write(str(date_mask[i]) + " " + str(len(tweets)) + "\n")
f.close()
