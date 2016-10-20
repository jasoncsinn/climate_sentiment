import numpy as np
import sqlite3
from random import shuffle

from sklearn.svm import LinearSVC,SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2,f_classif

from util import load_lines_from_file,parse_tweet

import pdb

LOC_TRAIN_DB = 'data/training_data.db'
LOC_OLD_TRAIN_DB = 'data/labelled_data.db'
LOC_PRED_DB = 'data/predicted_data.db'
PREDICT = False
USE_OLD_DATA = True 
PRINT_FEATURES = False
PRINT_FULL_TEST_RESULTS = False
PREDICT_TABLENAME = 'climate_2016_04_29'
PREDICT_FILENAME = 'data/full_tweet_data/' + PREDICT_TABLENAME + '.txt'

labelled_text = []
labelled_usable = []
labelled_sentiment = []
labelled_final = []

# Setup database connection and load data
conn = sqlite3.connect(LOC_TRAIN_DB)
c = conn.cursor()
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
#	shuffle(tweets)
	for row in tweets:
		labelled_text.append(row[0])
		labelled_usable.append(row[4])
		labelled_sentiment.append(row[5])
		labelled_final.append(row[6])
#	old_c.execute("SELECT * FROM vince_refined_tweets")
#	tweets = old_c.fetchall()
#	shuffle(tweets)
#	for row in tweets:
#		labelled_text.append(row[0])
#		labelled_usable.append(row[4])
#		labelled_sentiment.append(row[5])
#		labelled_final.append(row[6])
	old_conn.close()

# Partition into training vs. test data
#split_index = 3300 + 2610 + 1011
split_index = len(labelled_text) - 460
print(split_index)
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
#pdb.set_trace()

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
#pdb.set_trace()

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
		print(i + ' ' + j)
#print(len([i for i in test_Y if i == 's']))
num_correct = len([i for i,j in zip(prediction,test_Y) if i == j])
overall_acc = round(100.0*num_correct/len(prediction),4)
sentiment_clf_acc = round(100.0*overall_acc / usable_clf_acc)
print('Usable Classifier Accuracy: ' + str(usable_clf_acc) + '%')
print('Relevant Usable Classifier Accuracy: ' + str(relevant_usable_clf_acc) + '%')
print('Sentiment Classifier Accuracy: ' + str(sentiment_clf_acc) + '%')
print('Overall Accuracy: ' + str(overall_acc) + '%')
print('Relevant Accuracy: ' + str(relevant_usable_clf_acc * sentiment_clf_acc / 100.0) + '%')
#pdb.set_trace()

blacklist = ["#BustTheMyth :::", "Ricardo_AEA", "rainnwilson", "JettaH", "Crazy Bernie was the guy that claimed ISIS", "3803497941", "292785272", "BadManWizz", "1537476354", "726724131627122688", "Environment website::: Ricardo expert invited to Intergovernmental Panel", ":::FACE PALM::: x infinity!","25769092","166384151", "prassdfrimal","1495729418", "Are you f:::king kidding me.","3225213307", "jjasminnie","2371258508"]
def check_blacklist(tweet_str):
	check_components = tweet_str.split(':::')
#	pdb.set_trace()
	if len(check_components) != 6:
		return False
	for name in blacklist:
		if name in tweet_str:
			return False
	return True

# Predict
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
