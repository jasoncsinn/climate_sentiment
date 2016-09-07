def load_lines_from_file(filename):
	f = open(filename, 'r')
	ret = []
	for line in f:
		ret.append(line.strip())
	f.close()
	return ret

def merge_labelled_data(filename_X, filename_Y):
	lines_X = load_lines_from_file(filename_X)
	lines_Y = load_lines_from_file(filename_Y)
	sep = ' ::---:: '
	merged = [y + sep + x for x,y in zip(lines_X,lines_Y)]
	return merged

def split_labelled_data(filename):
	print('hi')
