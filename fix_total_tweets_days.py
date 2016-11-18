import datetime
import pdb

DATA_LOC = 'data/total_tweets.txt'

def extract_stats(line):
	date,num = line.split(" ",1)
	date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	num = int(num)
	return (date,num)

f = open(DATA_LOC, 'r')
lines = f.readlines()
f.close()

f = open('data/total_tweets_fixed.txt', 'w')

cur_index = 1
prev_index = 0

cdate,cnum = extract_stats(lines[cur_index])
pdate,pnum = extract_stats(lines[prev_index])

while cur_index < len(lines) - 1:
	if cdate == pdate:
		pnum += cnum
		cur_index += 1
		prev_index += 1
		cdate,cnum = extract_stats(lines[cur_index])
	else:
		f.write(str(pdate) + " " + str(pnum) + "\n")
		cur_index += 1
		prev_index += 1
		cdate,cnum = extract_stats(lines[cur_index])
		pdate,pnum = extract_stats(lines[prev_index])
f.close()
