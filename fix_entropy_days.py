import datetime
import pdb

def extract_stats(line):
	date, num = line.split(" ", 1)
	date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	num = float(num)
	return (date, num)

f = open('data/ambiguity_averages.txt', 'r')
lines = f.readlines()
f.close()

f = open('data/ambiguity_fixed.txt', 'w')
cur_index = 1
prev_index = 0

cdate, cnum = extract_stats(lines[cur_index])
pdate, pnum = extract_stats(lines[prev_index])

while cur_index < len(lines) - 1:
	if cdate == pdate:
		pnum = (pnum + cnum) / 2.0
		cur_index += 1
		prev_index += 1
		cdate,cnum = extract_stats(lines[cur_index])
	else:
		f.write(str(pdate) + " " + str(pnum) + "\n")
		cur_index += 1
		prev_index += 1
		cdate, cnum = extract_stats(lines[cur_index])
		pdate, pnum = extract_stats(lines[prev_index])
f.close()
