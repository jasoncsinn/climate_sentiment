import sqlite3
import operator
import string
from sklearn.feature_extraction import stop_words
import pdb

conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

table_name = raw_input("Enter table to read from (ex: climate_2015_01_01): ")
date = raw_input("Enter date to search for (ex: Jan 01): ")
sentiment = raw_input("Select sentiment to search for (a/s): ")
num_results = int(raw_input("Enter # of results to return: "))

to_execute = "SELECT * FROM "
to_execute += table_name
to_execute += " WHERE date LIKE '%"
to_execute += date
to_execute += "%' and sentiment='"
to_execute += sentiment
to_execute += "'"

c.execute(to_execute)
tweets = c.fetchall()

ht = {}
punct = set(string.punctuation)
sw = stop_words.ENGLISH_STOP_WORDS
custom_sw = ['global', 'warming', '', 'im']
for t in tweets:
	text = t[0]
	text = text.strip().split(' ')
	for word in text:
		word = ''.join(c for c in word if c not in punct)
		word = word.lower()
		ht[word] = ht.get(word, 0) + 1

for w in sw:
	if w in ht:
		del ht[w]
for w in custom_sw:
	if w in ht:
		del ht[w]

sorted_ht = sorted(ht.items(), key=operator.itemgetter(1), reverse=True)
print(str(sorted_ht[0:num_results]))
#pdb.set_trace()
