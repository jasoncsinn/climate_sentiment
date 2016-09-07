from util import load_lines_from_file, split_labelled_data
import json

import pdb

class Tweet():
	def __init__(self, text="", date="", twitterid=-1, screen_name="", location="", followers_count=-1, friends_count=-1, retweet_count=-1):
		self.date = date
		self.text = text
		self.twitterid = twitterid
		self.screen_name = screen_name
		self.location = location
		self.followers_count = followers_count
		self.friends_count = friends_count
		self.retweet_count = retweet_count
		self.label = ""

# NOTE THIS WILL ONLY WORK FOR TWEETS GIVEN IN THE FORM OF:
# {"created_at":"Fri Dec 11 05:00:20 +0000 2015":::text: "Sustainable Fire Engineering: After 9-11, Madrid, Mumbai, Tianjin, Paris + Climate Change \u2013 Shouldn't We All Now Be On The Same Wavelength ?":::id: 3401469783 :::screen name: sfe2016dublin","location":"Global":::followers count: 62,"friends_count":483:::retweet count: 0}
# This is not well formed json.
def load_tweet(input_string):
	input_string = input_string.strip().strip("{").strip("}")
	components = input_string.split(":::")
	if len(components) != 6:
		return None
	for comp in components:
		if comp.find(':') == -1:
			return None
	date = components[0].split(':')[1]
	text = components[1].split(':', 1)[1].strip().strip("\"")
	t = Tweet(text)
	return t

# Helper Function
def label_tweet(t):
	print("Tweet: " + t.text)
	label_input = raw_input("Choose (a)ctivist, (s)keptical, (n)eutral, (u)nusable, or e(x)it: ")
	if label_input == "a" or label_input == "activist":
		t.label = "activist"
	elif label_input == "s" or label_input == "skeptical":
		t.label = "skeptical"
	elif label_input == "n" or label_input == "neutral":
		t.label = "neutral"
	elif label_input == "x" or label_input == "exit":
		return False
	else:
		t.label = "unusable"
	return True

def label_and_save_tweets(t_list, filename):
	i = 0
	while (i < len(t_list) and label_tweet(t_list[i])):
		i += 1
	t_list = t_list[0:i]
	to_write = [t.label + ' ::---:: ' + t.text for t in t_list if t.label != "unusable"]
	f = open(filename, 'a')
	f.write("\n".join(to_write))
	f.close()	
	print("Saved.")

# Include list is conjunctive, exclude list is disjunctive. 
# the tweet must:
#	- contain all elements in include list 
#	- contain no elements in exclude list
def filter_tweets(t_list, include_list = [], exclude_list = []):
	new_t_list = []
	for t in t_list:
		filter_success = True
		for inc in include_list:
			if t.find(inc) == -1:
				filter_success = False
		for exc in exclude_list:
			if t.find(exc) != -1:
				filter_success = False
		if filter_success:
			new_t_list.append(t)
	return new_t_list

tweets = load_lines_from_file('data/full_tweet_data/climate_2016_05_06.txt', 10, 5)
t_list = [load_tweet(t_string) for t_string in tweets]
label_and_save_tweets(t_list, 'data/test_labelling.txt')
split_labelled_data('data/test_labelling.txt', 'data/test_labelling_x.txt', 'data/test_labelling_y.txt')

