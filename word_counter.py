import sqlite3
import operator
import string
import pdb
import datetime

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

from util import get_time_mask,make_word_ht

table_names,dates  = get_time_mask()
MODE = "u"
conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

stop_words = set(['climate','change','global','warming','climatechange','globalwarming'])

date_words_ht = {}
with open('data/word_counter/word_counter_' + MODE + '.txt', 'w') as f:
	for i in range(len(table_names)):
		cur_date = dates[i]
		end_date = dates[i+1]
		delta = datetime.timedelta(1)
		while cur_date <= end_date:
			to_execute = "SELECT * FROM "
			to_execute += table_names[i]
			to_execute += " WHERE date LIKE '%"
			to_execute += cur_date.strftime('%b %d')
			to_execute += "%' and sentiment='"
			to_execute += MODE
			to_execute += "'"

			c.execute(to_execute)
			word_ht = make_word_ht(c)
			print("Made word_ht for query: " + to_execute)
			sorted_words = sorted(word_ht.items(), key=operator.itemgetter(1), reverse=True)
			f.write(to_execute + "\n----------\n")
			for pair in sorted_words[:50]:
				if not pair[0] in ENGLISH_STOP_WORDS and not pair[0] in stop_words:
					f.write('word: ' + pair[0] + " num: " + str(pair[1]) + "\n")
			f.write("----------\n\n")
			print("Written to file.")
			cur_date += delta

