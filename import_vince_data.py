from util import load_lines_from_file
import sqlite3

conn = sqlite3.connect('data/labelled_data.db')
c = conn.cursor()

train_X = load_lines_from_file('data/train_tweets.txt')
train_Y = load_lines_from_file('data/train_sentiments.txt')

for text,label in zip(train_X,train_Y):
	text = text.replace("\'","")
	usable = 'n'
	sentiment = 'n'
	final_label = 'unusable'
	if label == 'skeptical':
		usable = 'y'
		sentiment = 's'
		final_label = 'skeptical'
	elif label == 'activist':
		usable = 'y'
		sentiment = 'a'
		final_label = 'activist'
	to_execute = "INSERT INTO vince_refined_tweets VALUES (\'" + text + "\',\'\',\'\',\'\',\'"
	to_execute += usable + "\',\'" + sentiment + "\',\'" + final_label + "\')"
	print(to_execute)
	c.execute(to_execute)
	conn.commit()
conn.close()
