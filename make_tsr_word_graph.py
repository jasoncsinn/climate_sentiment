import pdb
import datetime
import matplotlib.pyplot as plt

WORDS = ['trump', 'hoax', 'scandal', 'chinese', 'manufacturing']
WORD_INDEX = 4
INDEX_A = 2 + WORD_INDEX * 6 # index in line where to extract num for activists
INDEX_S = INDEX_A + 2
INDEX_N = INDEX_A + 4
# Example: 2015-01-01 word1 1 word2 2 word3 3
#		0	1   2   3   4   5   6
# INDEX = 4 -> get stats for word2
# Generally: word1 = 2, word2 = 8, word3 = 14, etc.
FILE = 'data/tsr_trump/word_counter_trump.txt'

def parse_date(date_str):
	return datetime.datetime.strptime(date_str,'%Y-%m-%d').date()

dates = []
acts = []
skes = []
others = []
with open(FILE) as f:
	for line in f:
		line = line.strip('\n').split(' ')
		date = parse_date(line[0])
		acts.append(int(line[INDEX_A]))
		skes.append(int(line[INDEX_S]))
		others.append(int(line[INDEX_N]))
		dates.append(date)

ax1 = plt.subplot(311)
ax2 = plt.subplot(312)
ax3 = plt.subplot(313)

ax1.plot_date(dates,acts,'-')
ax2.plot_date(dates,skes,'-')
ax3.plot_date(dates,others,'-')

title = "timeseries for word: " + WORDS[WORD_INDEX] + " from: " + str(dates[0]) + " to: " + str(dates[-1])
ax1.set_title('Activist ' + title)
ax2.set_title('Skeptic ' + title)
ax3.set_title('Other ' + title)

plt.tight_layout()
plt.show()
