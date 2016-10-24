import datetime
import pdb

DATA_LOC = 'data/timeseries_data.txt'

def extract_stats(line):
	date,act,ske = line.split(" ",2)
	date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	act = int(act)
	ske = int(ske)
	return (date,act,ske)

f = open(DATA_LOC, 'r')
lines = f.readlines()
f.close()

f = open('data/timeseries_data_fixed.txt', 'w')

cur_index = 1
prev_index = 0

cdate,cact,cske = extract_stats(lines[cur_index])
pdate,pact,pske = extract_stats(lines[prev_index])

while cur_index < len(lines) - 1:
	if cdate == pdate:
		pact += cact
		pske += cske
		cur_index += 1
		prev_index += 1
		cdate,cact,cske = extract_stats(lines[cur_index])
	else:
		f.write(str(pdate) + " " + str(pact) + " " + str(pske) + "\n")
		cur_index += 1
		prev_index += 1
		cdate,cact,cske = extract_stats(lines[cur_index])
		pdate,pact,pske = extract_stats(lines[prev_index])
f.close()
