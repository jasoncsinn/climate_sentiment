import pdb
import datetime

from util import get_time_mask, tweet_date

linenum = 1
ht = {}
sentiments = ['a', 's', 'n']

words_bn_khaled = ['concerned', 'khaled', 'nye']
files_bn_khaled = ['data/tsr_bn_khaled/sentiments_bn_khaled_pre.txt',
		'data/tsr_bn_khaled/sentiments_bn_khaled_post.txt',
		'data/tsr_bn_khaled/word_counter_bn_khaled.txt']
words_cop21 = ['obama', 'paris', 'cop21']
files_cop21 = ['data/tsr_cop21/sentiments_cop21_pre.txt',
		'data/tsr_cop21/sentiments_cop21_post.txt',
		'data/tsr_cop21/word_counter_cop21.txt']
words_dicaprio = ['leonardo', 'dicaprio', 'oscar']
files_dicaprio = ['data/tsr_dicaprio/sentiments_dicaprio_pre.txt',
		'data/tsr_dicaprio/sentiments_dicaprio_post.txt',
		'data/tsr_dicaprio/word_counter_dicaprio.txt']
words_earthday = ['earth', 'day']
files_earthday = ['data/tsr_earthday/sentiments_earthday_pre.txt',
		'data/tsr_earthday/sentiments_earthday_post.txt',
		'data/tsr_earthday/word_counter_earthday.txt']
words_trump = ['trump', 'hoax', 'scandal', 'chinese', 'manufacturing']
files_trump = ['data/tsr_trump/sentiments_trump_pre.txt',
		'data/tsr_trump/sentiments_trump_post.txt',
		'data/tsr_trump/word_counter_trump.txt']

# ht = { word1: { day: num, }, word2: { day: num, }}
#words = words_bn_khaled
#files = files_bn_khaled
#words = words_cop21
#files = files_cop21
#words = words_dicaprio
#files = files_dicaprio
#words = words_earthday
#files = files_earthday
words = words_trump
files = files_trump

with open(files[0]) as f:
	for line in f:
		line = line.strip('\n')
		tweet_str, date_str, _, _, sentiment = line.split(" ::---:: ", 4)
		for word in words:
			if word in tweet_str:
				date = tweet_date(date_str)
				date_ht = ht.get(date, {})
				num = date_ht.get(word + "-" + sentiment, 0) + 1
				date_ht[word + "-" + sentiment] = num
				ht[date] = date_ht
		linenum += 1

with open(files[1]) as f:
	for line in f:
		line = line.strip('\n')
		tweet_str, date_str, _, _, sentiment = line.split(" ::---:: ", 4)
		for word in words:
			if word in tweet_str:
				date = tweet_date(date_str)
				date_ht = ht.get(date, {})
				num = date_ht.get(word + "-" + sentiment, 0) + 1
				date_ht[word + "-" + sentiment] = num
				ht[date] = date_ht
		linenum += 1

with open(files[2], 'w') as f:
	for date in sorted(ht.keys()):
		date_ht = ht[date]
		texts = []
		for word in words:
			for sent in sentiments:
				texts.append(word + "-" + sent + " " + str(date_ht.get(word + "-" + sent, 0)))
		to_write = str(date) + " " + " ".join(texts)
		print(to_write)
		f.write(to_write + "\n")
