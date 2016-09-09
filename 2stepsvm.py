import numpy as np
import sqlite3

from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer

import pdb

LOC_DB = 'data/labelled_data.db'


labelled_text = []
labelled_usable = []
labelled_sentiment = []
labelled_final = []

# Setup database connection and load data
conn = sqlite3.connect(LOC_DB)
c = conn.cursor()
for row in c.execute("SELECT * FROM vince_tweets"):
	labelled_text.append(row[0])
	labelled_usable.append(row[4])
	labelled_sentiment.append(row[5])
	labelled_final.append(row[6])
conn.close()

# Partition into training vs. test data
train_usable_X = labelled_text[0:900]
train_usable_Y = labelled_usable[0:900]
train_sentiment_X = [i for i,j in zip(labelled_text[0:900], labelled_sentiment[0:900]) if j != 'n']
train_sentiment_Y = [j for j in labelled_sentiment[0:900] if j != 'n']
test_X = labelled_text[900:]
test_Y = labelled_sentiment[900:]

# Extract features for usable classifier
usable_cv = CountVectorizer()
usable_cv = usable_cv.fit(train_usable_X)
usable_train_dtmatrix = usable_cv.transform(train_usable_X)

# Train usable classifier
usable_clf = SVC(C=0.1,kernel='linear')
usable_clf.fit(usable_train_dtmatrix, train_usable_Y)

# Extract features for sentiment classifier
sentiment_cv = CountVectorizer()
sentiment_cv = sentiment_cv.fit(train_sentiment_X)
sentiment_train_dtmatrix = sentiment_cv.transform(train_sentiment_X)

# Train sentiment classifier
sentiment_clf = SVC()
sentiment_clf.fit(sentiment_train_dtmatrix, train_sentiment_Y)

# Test
usable_test_dtmatrix = usable_cv.transform(test_X)
prediction = usable_clf.predict(usable_test_dtmatrix)
sentiment_test_dtmatrix = sentiment_cv.transform([i for i,j in zip(test_X, prediction) if j == 'y'])
sentiment_prediction = sentiment_clf.predict(sentiment_test_dtmatrix)
sentiment_indices = [i for i in range(len(prediction)) if prediction[i] == 'y']
j = 0
for i in sentiment_indices:
	prediction[i] = sentiment_prediction[j]
	j += 1
num_correct = len([i for i,j in zip(prediction,test_Y) if i == j])
print('Num correct: ' + str(num_correct))
print('Num test cases: ' + str(len(prediction)))
print('Accuracy: ' + str(round(100.0*num_correct/len(prediction),4)) + '%')
#pdb.set_trace()

