import numpy as np
import sqlite3
from random import shuffle
import matplotlib.pyplot as plt

from sklearn.svm import LinearSVC,SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2,f_classif

from util import load_lines_from_file,parse_tweet,get_time_mask

import pdb
import sys

# Logger
class Logger(object):
	def __init__(self):
		self.terminal = sys.stdout
		self.log = open("data/2stepsvm.log", "a")
	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
	def flush(self):
		pass
#sys.stdout = Logger()

# Flags
LOC_TRAIN_DB = 'data/refined_training_data.db'
LOC_OLD_TRAIN_DB = 'data/labelled_data.db'
LOC_PRED_DB = 'data/predicted_data.db'
USE_OLD_DATA = True
PRINT_FEATURES = False
PRINT_FULL_VALIDATION_RESULTS = False
PRINT_CONFUSION_MATRIX = True
PREDICT = False
PREDICT_TABLE_NAMES,_ = get_time_mask()
PREDICT_BATCH_SIZE = 1000
stop_words = ['global', 'warming', 'globalwarming', 'climate', 'climate', 'climatechange', 'http', 'https']
PLOT_NUM_FEATURES = False

# Setup database connection and load data
conn = sqlite3.connect(LOC_TRAIN_DB)
c = conn.cursor()
c.execute("SELECT * FROM training")
tr_d = c.fetchall()
c.execute("SELECT * FROM test")
te_d = c.fetchall()
c.execute("SELECT * FROM validation")
va_d = c.fetchall()

#shuffle(tr_d)

tr_a = [d for d in tr_d if d[2] == 'a']
tr_s = [d for d in tr_d if d[2] == 's']
tr_o = [d for d in tr_d if d[2] == 'n']

tr_d = np.concatenate((tr_a[:800],tr_s[:800],tr_o[:800]), axis=0).tolist()

#for data in tr_d:
#	c.execute("INSERT INTO refined_training VALUES ('" + data[0] + "','" + data[1] + "','" + data[2] + "')")

#conn.commit()

tr_x = [d[0] for d in tr_d]
tr_y_ = [d[2] for d in tr_d]
te_x = [d[0] for d in te_d]
te_y_ = [d[2] for d in te_d]
va_x = [d[0] for d in va_d]
va_y_ = [d[2] for d in va_d]

pdb.set_trace()

x = range(1000,1001)
if PLOT_NUM_FEATURES:
	x = range(1,5000,50)
	y = []
for num_features in x:	
	#Extract features
	cv = CountVectorizer(stop_words=stop_words)
	cv = cv.fit(tr_x)
	tr_dtmat = cv.transform(tr_x)
	sel = SelectKBest(chi2,k=num_features)
	tr_dtmat = sel.fit_transform(tr_dtmat,tr_y_)

	if PRINT_FEATURES:
		feature_list = cv.get_feature_names()
		feature_map = sel.get_support()
		features = [i for i,j in zip(feature_list, feature_map) if j == True]
		print("Features: " + ','.join(features))

	# Train
	clf = LinearSVC(penalty='l2')
	clf.fit(tr_dtmat.toarray(),tr_y_)
	
	# Validate
	va_dtmat = cv.transform(va_x)
	va_dtmat = sel.transform(va_dtmat)
	predicted = clf.predict(va_dtmat)

	if PRINT_FULL_VALIDATION_RESULTS:
		for i,j,k in zip(predicted,va_y_, va_x):
			print("Predicted: " + i + " Actual: " + j + " Text: " + k)

	va_acc = 100.0 * clf.score(va_dtmat, va_y_)
	print("Validation Accuracy: " + str(va_acc) + " num_features: " + str(num_features))
	if PLOT_NUM_FEATURES:
		y.append(va_acc)

	if PRINT_CONFUSION_MATRIX:
		mat = np.zeros((3,3), dtype=int)
		preds = ['a', 's', 'n']
		acts = ['a', 's', 'n']
		for pred,act in zip(predicted,va_y_):
			for i,actual in enumerate(acts):
				for j,predict in enumerate(preds):
					if pred == predict and act == actual:
						mat[i,j] += 1
		print(mat)

if PLOT_NUM_FEATURES:
	ax = plt.subplot(111)
	ax.plot(x,y,'-')
	plt.show()
'''

labelled_text = []
labelled_usable = []
labelled_sentiment = []
labelled_final = []

c.execute("SELECT * FROM tweets")
tweets = c.fetchall()
#shuffle(tweets)
for row in tweets:
	labelled_text.append(row[0])
	labelled_usable.append(row[4])
	labelled_sentiment.append(row[5])
	labelled_final.append(row[6])
conn.close()
if USE_OLD_DATA:
	old_conn = sqlite3.connect(LOC_OLD_TRAIN_DB)
	old_c = old_conn.cursor()
	old_c.execute("SELECT * FROM vince_refined_tweets")
	tweets = old_c.fetchall()
#	shuffle(tweets)
	for row in tweets:
		labelled_text.append(row[0])
		labelled_usable.append(row[4])
		labelled_sentiment.append(row[5])
		labelled_final.append(row[6])
	old_c.execute("SELECT * FROM tweets")
	tweets = old_c.fetchall()
	shuffle(tweets)
	for row in tweets:
		labelled_text.append(row[0])
		labelled_usable.append(row[4])
		labelled_sentiment.append(row[5])
		labelled_final.append(row[6])
	old_conn.close()

# Partition into training vs. test data
split_index = len(labelled_text) - 460
print("Training set size: " + str(split_index))
train_usable_X = labelled_text[0:split_index]
train_usable_Y = labelled_usable[0:split_index]
train_sentiment_X = [i for i,j in zip(labelled_text[0:split_index], labelled_sentiment[0:split_index]) if j != 'n']
train_sentiment_Y = [j for j in labelled_sentiment[0:split_index] if j != 'n']
test_X = labelled_text[split_index:]
test_Y = labelled_sentiment[split_index:]

# Extract features for usable classifier
usable_cv = CountVectorizer(stop_words='english',ngram_range=(1,3),min_df=2)
usable_cv = usable_cv.fit(train_usable_X)
usable_train_dtmatrix = usable_cv.transform(train_usable_X)
sel = SelectKBest(chi2,k=10000)
usable_train_dtmatrix = sel.fit_transform(usable_train_dtmatrix, train_usable_Y)
if PRINT_FEATURES:
	feature_list = usable_cv.get_feature_names()
	feature_map = sel.get_support()
	features = [i for i,j in zip(feature_list, feature_map) if j == True]
	print("Features: ", features)

# Train usable classifier
usable_clf = BernoulliNB()
usable_clf.fit(usable_train_dtmatrix.toarray(), train_usable_Y)

# Test usable classifier
usable_test_Y = labelled_usable[split_index:]
usable_test_dtmatrix = usable_cv.transform(test_X)
usable_test_dtmatrix = sel.transform(usable_test_dtmatrix)
usable_clf_acc = 100.0*usable_clf.score(usable_test_dtmatrix.toarray(), usable_test_Y)
results = usable_clf.predict(usable_test_dtmatrix.toarray())
false_positives = [predict for predict,real in zip(results,usable_test_Y) if predict == 'y' and real == 'n']
false_negatives = [predict for predict,real in zip(results,usable_test_Y) if predict == 'n' and real == 'y']
#print(" ".join(false_positives))
#print(" ".join(false_negatives))
#print(len(usable_test_Y))
relevant_usable_clf_acc = (100.0*(len(usable_test_Y) - len(false_positives)))/len(usable_test_Y)

# Extract features for sentiment classifier
sentiment_cv = CountVectorizer()
sentiment_cv = sentiment_cv.fit(train_sentiment_X)
sentiment_train_dtmatrix = sentiment_cv.transform(train_sentiment_X)

# Train sentiment classifier
sentiment_clf = LinearSVC()
sentiment_clf.fit(sentiment_train_dtmatrix, train_sentiment_Y)

# Test Overall
usable_test_dtmatrix = usable_cv.transform(test_X)
usable_test_dtmatrix = sel.transform(usable_test_dtmatrix)
prediction = usable_clf.predict(usable_test_dtmatrix.toarray())
sentiment_test_dtmatrix = sentiment_cv.transform([i for i,j in zip(test_X, prediction) if j == 'y'])
sentiment_prediction = sentiment_clf.predict(sentiment_test_dtmatrix)
sentiment_indices = [i for i in range(len(prediction)) if prediction[i] == 'y']
j = 0
for i in sentiment_indices:
	prediction[i] = sentiment_prediction[j]
	j += 1
if PRINT_FULL_TEST_RESULTS:
	for i,j in zip(prediction,test_Y):
		print(i + " " + j)

if PRINT_CONFUSION_MATRIX:
	mat = np.zeros((3,3), dtype=int)
	preds = ['a', 's', 'n']
	acts = ['a', 's', 'n']
	for pred,act in zip(prediction,test_Y):
		for i,actual in enumerate(acts):
			for j,predict in enumerate(preds):
				if pred == predict and act == actual:
					mat[i,j] += 1
	print(mat)

num_correct = len([i for i,j in zip(prediction,test_Y) if i == j])
overall_acc = round(100.0*num_correct/len(prediction),4)
sentiment_clf_acc = round(100.0*overall_acc / usable_clf_acc)
print('Usable Classifier Accuracy: ' + str(usable_clf_acc) + '%')
print('Relevant Usable Classifier Accuracy: ' + str(relevant_usable_clf_acc) + '%')
print('Sentiment Classifier Accuracy: ' + str(sentiment_clf_acc) + '%')
print('Overall Accuracy: ' + str(overall_acc) + '%')
print('Relevant Accuracy: ' + str(relevant_usable_clf_acc * sentiment_clf_acc / 100.0) + '%')

blacklist = []
def check_blacklist(tweet_str):
	check_components = tweet_str.split(':::')
	if len(check_components) != 6:
		return False
	for name in blacklist:
		if name in tweet_str:
			return False
	return True

# Predict
if PREDICT:
	with sqlite3.connect(LOC_PRED_DB) as pred_conn:
		pred_c = pred_conn.cursor()

		for table_name in PREDICT_TABLE_NAMES[68:]:
			cur_line = 1
			fn = 'data/full_tweet_data/' + table_name + '.txt'
			tweets = load_lines_from_file(fn, PREDICT_BATCH_SIZE, cur_line)
			while len(tweets) > 0:
				print('Inferring sentiment with tweet #' + str(cur_line) + ' from ' + table_name)
				texts = []
				dates = []
				usernames = []
				locations = []
				for tweet_str in tweets:
					if check_blacklist(tweet_str):
						date, text, username, location = parse_tweet(tweet_str)
						dates.append(date)
						texts.append(text)
						usernames.append(username)
						locations.append(location)
				predict_dtmatrix = usable_cv.transform(texts)
				predict_dtmatrix = sel.transform(predict_dtmatrix)
				prediction = usable_clf.predict(predict_dtmatrix.toarray())

				sentiment_predict_dtmatrix = sentiment_cv.transform([i for i,j in zip(texts, prediction) if j == 'y'])
				sentiment_prediction = sentiment_clf.predict(sentiment_predict_dtmatrix)
				sentiment_indices = [i for i in range(len(prediction)) if prediction[i] == 'y']
				j = 0
				for i in sentiment_indices:
					prediction[i] = sentiment_prediction[j]
					j += 1
				
				for i in range(len(texts)):
					to_execute = "INSERT INTO " + table_name + " VALUES (\'"
					to_execute += texts[i] + "\',\'" 
					to_execute += dates[i] + "\',\'"
					to_execute += usernames[i] + "\',\'" 
					to_execute += locations[i] + "\',\'" 
					to_execute += prediction[i] + "\')"
					pred_c.execute(to_execute)
					pred_conn.commit()

				cur_line += PREDICT_BATCH_SIZE
				tweets = load_lines_from_file(fn, PREDICT_BATCH_SIZE, cur_line)
'''
'''
cur_line = 1
batch_size = 1000
while(PREDICT and cur_line < 1000000):
	tweets = load_lines_from_file(PREDICT_FILENAME, batch_size, cur_line)
	dates = []
	texts = []
	usernames = []
	locations = []
	for tweet_str in tweets:
		#print(tweet_str)
		if check_blacklist(tweet_str):
			date, text, username, location = parse_tweet(tweet_str)
			dates.append(date)
			texts.append(text)
			usernames.append(username)
			locations.append(location)
		#print(date + " - " + username + ": " + text)
	#pdb.set_trace()
	predict_dtmatrix = usable_cv.transform(texts)
	predict_dtmatrix = sel.transform(predict_dtmatrix)
	prediction = usable_clf.predict(predict_dtmatrix.toarray())
	sentiment_predict_dtmatrix = sentiment_cv.transform([i for i,j in zip(texts, prediction) if j == 'y'])
	sentiment_prediction = sentiment_clf.predict(sentiment_predict_dtmatrix)
	sentiment_indices = [i for i in range(len(prediction)) if prediction[i] == 'y']
	j = 0
	for i in sentiment_indices:
		prediction[i] = sentiment_prediction[j]
		j += 1
	pred_conn = sqlite3.connect(LOC_PRED_DB)
	pred_c = pred_conn.cursor()
	for i in range(len(texts)):
		to_execute = "INSERT INTO " + PREDICT_TABLENAME + " VALUES (\'" + texts[i] + "\',\'" + dates[i] + "\',\'" + usernames[i] + "\',\'" + locations[i] + "\',\'" + prediction[i] + "\')"
		pred_c.execute(to_execute)
	pred_conn.commit()
	print("Commited from cur line: " + str(cur_line))
	pred_conn.close()
	print("Connection closed. Exiting.")
	cur_line += 1000
'''
