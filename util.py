import datetime
from os import listdir
import re

def tweet_datetime(s):
	return datetime.datetime.strptime(s, '%a %b %d %H:%M:%S +0000 %Y')

def tweet_date(s):
	return tweet_datetime(s).date()

def load_lines_from_file(filename, max_lines=-1, start_line=1):
	f = open(filename, 'r')
	ret = []
	j = 1
	while j < start_line:
		f.readline()
		j += 1
	if max_lines == -1:
		for line in f:
			ret.append(line.strip())
	else:
		i = 0
		line = f.readline()
		while i < max_lines and line != '':
			ret.append(line.strip())
			line = f.readline()
			i += 1
	f.close()
	return ret

def get_time_mask():
	table_names = [t.strip('.txt') for t in listdir('data/full_tweet_data')]
	table_names.sort()
	dates = [datetime.date(2015,4,7)]
	for table_name in table_names:
		dt = datetime.datetime.strptime(table_name,'climate_%Y_%m_%d').date()
		dates.append(dt)
	return (table_names, dates)

def can_parse(tweet_str, blacklist):
	check_components = tweet_str.split(':::')
	if len(check_components) != 6:
		return False
	for name in blacklist:
		if name in tweet_str:
			return False
	return True

def parse_tweet(tweet_str):
	tweet_str = tweet_str.strip().strip("{").strip("}")
	components = tweet_str.split(":::")
	date = components[0].split(':',1)[1].strip().strip("\"")
	text = components[1].split(':',1)[1].strip().strip("\"").replace("\'","")
	username = components[3].split(',',1)[0].split(':',1)[1].strip().strip("\"")
	location = components[3].split(',',1)[1].split(':',1)[1].strip().strip("\"").replace("\'","")
	return (date, text, username, location)

# helper for process_text
def remove_links(tokens):
        to_remove = []
        for i in range(len(tokens)):
                if "http" in tokens[i] or "https" in tokens[i]:
                        to_remove.append(i)
        for i in sorted(to_remove, reverse=True):
                del tokens[i]
        return tokens

# helper for process_text
def remove_retweet(tokens):
        if len(tokens) > 2 and tokens[0] == "rt":
                del tokens[1]
                del tokens[0]
        return tokens

# helper for process_text
def replace_unicode(text):
        text = text.replace('\\u2018', '\'')
        text = text.replace('\\u2019', '\'')
        text = text.replace('\\u2026', '...')
        text = text.replace('\\u00a0', ' ')
        text = text.replace('\\\"', '')
        text = re.sub("\\\\u....", '', text)
        return text

# stop_words should be a set
def process_text(text, stop_words):
        text = replace_unicode(text)
        tokens = re.split(' |\n|,|\\\\n|=', text)
        tokens = remove_links(tokens)
        tokens = [t.lower() for t in tokens]
        tokens = remove_retweet(tokens)
        tokens = [t.strip(',.?\'":;[]{}-_()!~|') for t in tokens]
        tokens = [t for t in tokens if not t in stop_words]
        tokens = [t for t in tokens if t != '']
        return ' '.join(tokens)

# db_itr most likely cursor after execute
def make_word_ht(db_itr):
        word_ht = {}
        for i,row in enumerate(db_itr):
                text, date, username, location, sent = row
                processed_text = process_text(text, set())
                tokens = processed_text.split(' ')
                for token in tokens:
                        word_ht[token] = word_ht.get(token, 0) + 1
        return word_ht
