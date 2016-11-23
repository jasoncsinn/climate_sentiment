import pdb
import operator

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

word_ht = {}

with open('data/word_data_deniers.txt') as f:
	for line in f:
		word, num = line.split(' ')
		if not word in ENGLISH_STOP_WORDS:
			word_ht[word] = int(num.strip('\n'))

sorted_words = sorted(word_ht.items(), key=operator.itemgetter(1), reverse=True)

for pair in sorted_words[:100]:
	print(pair[0] + " " + str(pair[1]))

#pdb.set_trace()
