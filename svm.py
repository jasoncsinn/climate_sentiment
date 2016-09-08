import numpy as np
import codecs
import sys
import pickle
import time

from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer

from util import load_lines_from_file, save_incorrect_tweets
import pdb

LOC_TRAIN_X = 'data/train_x.txt'
LOC_TRAIN_Y = 'data/train_y.txt'
LOC_TRAIN_NEW_X = 'data/label_05_06_x.txt'
LOC_TRAIN_NEW_Y = 'data/label_05_06_y.txt'
LOC_TEST_X = 'data/test_x.txt'
LOC_TEST_Y = 'data/test_y.txt'
LOC_FEATURE_LIST = 'data/feature_list.txt'

# Load data
train_X = load_lines_from_file(LOC_TRAIN_X)
train_Y = load_lines_from_file(LOC_TRAIN_Y)
train_X += load_lines_from_file(LOC_TRAIN_NEW_X)
train_Y += load_lines_from_file(LOC_TRAIN_NEW_Y)
test_X = load_lines_from_file(LOC_TEST_X)
test_Y = load_lines_from_file(LOC_TEST_Y)
#test_X = load_lines_from_file(LOC_TRAIN_NEW_X)
#test_Y = load_lines_from_file(LOC_TRAIN_NEW_Y)

# Extract features
cv = CountVectorizer()
cv = cv.fit(train_X)
train_dtmatrix = cv.transform(train_X)
feature_list = cv.get_feature_names()
feature_writer = open(LOC_FEATURE_LIST, 'w')
feature_writer.write("\n".join(feature_list))
feature_writer.close()

# Train
clf = SVC()
#params_space = { 'C': np.logspace(-5, 0, 10), 'class_weight':[None,'balanced']}
#gscv = GridSearchCV(clf, params_space, cv=2)
#gscv.fit(train_dtmatrix, train_Y)
clf.fit(train_dtmatrix, train_Y)

# Test
test_dtmatrix = cv.transform(test_X)
print(clf.score(test_dtmatrix, test_Y))
#prediction = gscv.predict(test_dtmatrix)

#save_incorrect_tweets('data/incorrect_tweets_original.txt', test_X, test_Y, prediction)
#num_correct = len([i for i, j in zip(prediction, test_Y) if i == j])
#print('Num correct: ' + str(num_correct))
#print('# of Test Cases: ' + str(len(prediction)))
#print('Accuracy: ' + str(round(100.0*num_correct/len(prediction), 4)) + '%')

