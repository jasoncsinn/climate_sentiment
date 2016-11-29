import datetime
import pdb

def extract_stats(line):
	date, avg_a, avg_s, avg_n, avg_u, avg_nu = line.split(" ", 5)
	date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	avg_a = float(avg_a)
	avg_s = float(avg_s)
	avg_n = float(avg_n)
	avg_u = float(avg_u)
	avg_nu = float(avg_nu)

	return (date, avg_a, avg_s, avg_n, avg_u, avg_nu)

f = open('data/ambiguity_by_sentiment.txt', 'r')
lines = f.readlines()
f.close()

f = open('data/ambiguity_sentiment_fixed.txt', 'w')
cur_index = 1
prev_index = 0

cdate, cavg_a, cavg_s, cavg_n, cavg_u, cavg_nu = extract_stats(lines[cur_index])
pdate, pavg_a, pavg_s, pavg_n, pavg_u, pavg_nu = extract_stats(lines[prev_index])

while cur_index < len(lines) - 1:
	if cdate == pdate:
		pavg_a = (pavg_a + cavg_a) / 2.0
		pavg_s = (pavg_s + cavg_s) / 2.0
		pavg_n = (pavg_n + cavg_n) / 2.0
		pavg_u = (pavg_u + cavg_u) / 2.0
		pavg_nu = (pavg_nu + cavg_nu) / 2.0

		cur_index += 1
		prev_index += 1
		cdate, cavg_a, cavg_s, cavg_n, cavg_u, cavg_nu = extract_stats(lines[cur_index])
	else:
		f.write(str(pdate) + " " + str(pavg_a) + ' ' + str(pavg_s) + ' ' + str(pavg_n) + ' ' + str(pavg_u) + ' ' + str(pavg_nu) + "\n")
		cur_index += 1
		prev_index += 1
		cdate, cavg_a, cavg_s, cavg_n, cavg_u, cavg_nu = extract_stats(lines[cur_index])
		pdate, pavg_a, pavg_s, pavg_n, pavg_u, pavg_nu = extract_stats(lines[prev_index])
f.close()
