import numpy as np
import sqlite3
from random import shuffle

from sklearn.svm import LinearSVC,SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2,f_classif

import pdb

LOC_DB = 'data/labelled_data.db'

labelled_text = []
labelled_usable = []
labelled_sentiment = []
labelled_final = []

# Setup database connection and load data
conn = sqlite3.connect(LOC_DB)
c = conn.cursor()
c.execute("SELECT * FROM tweets")
tweets = c.fetchall()
shuffle(tweets)
for row in tweets:
	labelled_text.append(row[0])
	labelled_usable.append(row[4])
	labelled_sentiment.append(row[5])
	labelled_final.append(row[6])
#c.execute("SELECT * FROM vince_refined_tweets")
#tweets = c.fetchall()
#shuffle(tweets)
#for row in tweets:
#	labelled_text.append(row[0])
#	labelled_usable.append(row[4])
#	labelled_sentiment.append(row[5])
#	labelled_final.append(row[6])
#c.execute("SELECT * FROM tweets")
#tweets = c.fetchall()
#shuffle(tweets)
#for row in tweets:
#	labelled_text.append(row[0])
#	labelled_usable.append(row[4])
#	labelled_sentiment.append(row[5])
#	labelled_final.append(row[6])
conn.close()

#print(" ".join(labelled_sentiment))


# Partition into training vs. test data
split_index = 900
train_usable_X = labelled_text[0:split_index]
train_usable_Y = labelled_usable[0:split_index]
train_sentiment_X = [i for i,j in zip(labelled_text[0:split_index], labelled_sentiment[0:split_index]) if j != 'n']
train_sentiment_Y = [j for j in labelled_sentiment[0:split_index] if j != 'n']
test_X = labelled_text[split_index:]
test_Y = labelled_sentiment[split_index:]

# Extract features for usable classifier
usable_cv = CountVectorizer()
usable_cv = usable_cv.fit(train_usable_X)
usable_train_dtmatrix = usable_cv.transform(train_usable_X)
sel = SelectKBest(chi2,k=50)
usable_train_dtmatrix = sel.fit_transform(usable_train_dtmatrix, train_usable_Y)
feature_list = usable_cv.get_feature_names()
feature_map = sel.get_support()
features = [i for i,j in zip(feature_list, feature_map) if j == True]
print("Features: " + " ".join(features))
#pdb.set_trace()

# Train usable classifier
#usable_clf = SVC(C=0.1,kernel='linear')
usable_clf = BernoulliNB()
usable_clf.fit(usable_train_dtmatrix.toarray(), train_usable_Y)

# Test usable classifier
usable_test_Y = labelled_usable[split_index:]
usable_test_dtmatrix = usable_cv.transform(test_X)
usable_test_dtmatrix = sel.transform(usable_test_dtmatrix)
usable_clf_acc = 100.0*usable_clf.score(usable_test_dtmatrix.toarray(), usable_test_Y)

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
#for i,j in zip(prediction,test_Y):
#	print(i + ' ' + j)
#print(len([i for i in test_Y if i == 's']))
num_correct = len([i for i,j in zip(prediction,test_Y) if i == j])
overall_acc = round(100.0*num_correct/len(prediction),4)
sentiment_clf_acc = round(100.0*overall_acc / usable_clf_acc)
print('Usable Classifier Accuracy: ' + str(usable_clf_acc) + '%')
print('Sentiment Classifier Accuracy: ' + str(sentiment_clf_acc) + '%')
print('Overall Accuracy: ' + str(overall_acc) + '%')
#pdb.set_trace()

