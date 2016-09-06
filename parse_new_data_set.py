import pdb

f = open('data/tweets_sentiment_refined.txt')
data_x = []
data_y = []
for line in f:
	linelist = line.split('::---::', 2)
	data_y.append(linelist[0].strip())
	data_x.append(linelist[1].strip())
f.close()
pdb.set_trace()

data_X = open('data/x_refined.txt', 'w')
data_X.write("\n".join(data_x))
data_X.close()

data_Y = open('data/y_refined.txt', 'w')
data_Y.write("\n".join(data_y))
data_Y.close()
