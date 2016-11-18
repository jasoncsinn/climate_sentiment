import datetime
from os import listdir

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

def merge_labelled_data(filename_X, filename_Y):
	lines_X = load_lines_from_file(filename_X)
	lines_Y = load_lines_from_file(filename_Y)
	sep = ' ::---:: '
	merged = [y + sep + x for x,y in zip(lines_X,lines_Y)]
	return merged

def split_labelled_data(filename, filename_X, filename_Y):
	f = open(filename)
	X = []
	Y = []
	for line in f:
		linelist = line.split('::---::', 1)
		Y.append(linelist[0].strip())
		X.append(linelist[1].strip())
	f.close()
	f_X = open(filename_X, 'w')
	f_X.write("\n".join(X))
	f_X.close()

	f_Y = open(filename_Y, 'w')
	f_Y.write("\n".join(Y))
	f_Y.close()
	return (X,Y)

def save_incorrect_tweets(filename, test_X, test_Y, prediction):
	incorrect = []
	for i in range(len(test_X)):
		if prediction[i] != test_Y[i]:
			incorrect.append(test_Y[i] + " ::---:: " + prediction[i] + "::---:: " + test_X[i])
	f = open(filename, 'w')
	f.write("\n".join(incorrect))
	f.close()
