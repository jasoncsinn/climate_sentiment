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

def get_db_info():
	table_names = ['climate_2016_01_01','climate_2016_01_08','climate_2016_01_15','climate_2016_01_22','climate_2016_01_29','climate_2016_02_05','climate_2016_02_12','climate_2016_02_19','climate_2016_02_26','climate_2016_03_04','climate_2016_03_11','climate_2016_03_18','climate_2016_03_25','climate_2016_04_01','climate_2016_04_08','climate_2016_04_15','climate_2016_04_22','climate_2016_04_29','climate_2016_05_06','climate_2016_05_13','climate_2016_05_20','climate_2016_05_27','climate_2016_06_03','climate_2016_06_10','climate_2016_06_17','climate_2016_06_24','climate_2016_07_01','climate_2016_07_08','climate_2016_07_15','climate_2016_07_22','climate_2016_07_29','climate_2016_08_05','climate_2016_08_12','climate_2016_08_19','climate_2016_08_26','climate_2016_09_02','climate_2016_09_09','climate_2016_09_16','climate_2016_09_23','climate_2016_09_30','climate_2016_10_07']
	dates = [datetime.date(2015,12,25),datetime.date(2016,1,1),datetime.date(2016,1,8),datetime.date(2016,1,15),datetime.date(2016,1,22),datetime.date(2016,1,29),datetime.date(2016,2,5),datetime.date(2016,2,12),datetime.date(2016,2,19),datetime.date(2016,2,26),datetime.date(2016,3,4),datetime.date(2016,3,11),datetime.date(2016,3,18),datetime.date(2016,3,25),datetime.date(2016,4,1),datetime.date(2016,4,8),datetime.date(2016,4,15),datetime.date(2016,4,22),datetime.date(2016,4,29),datetime.date(2016,5,6),datetime.date(2016,5,13),datetime.date(2016,5,20),datetime.date(2016,5,27),datetime.date(2016,6,3),datetime.date(2016,6,10),datetime.date(2016,6,17),datetime.date(2016,6,24),datetime.date(2016,7,1),datetime.date(2016,7,8),datetime.date(2016,7,15),datetime.date(2016,7,22),datetime.date(2016,7,29),datetime.date(2016,8,5),datetime.date(2016,8,12),datetime.date(2016,8,19),datetime.date(2016,8,26),datetime.date(2016,9,2),datetime.date(2016,9,9),datetime.date(2016,9,16),datetime.date(2016,9,23),datetime.date(2016,9,30),datetime.date(2016,10,7)]
	return (table_names, dates)

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
