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
