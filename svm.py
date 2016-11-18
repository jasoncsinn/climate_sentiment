import numpy as np
import sqlite3
import matplotlib.pyplot as plt

from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest,chi2
from sklearn.calibration import CalibratedClassifierCV

from text_processor import process_text

import pdb
import sys

LOC_TRAIN_DB = 'data/refined_training_data.db'
LOC_LOG = 'data/svm.log'
LOG_ENABLED = False
PRINT_FULL_RESULTS = False
PRINT_CONFUSION_MATRIX = True
PRINT_FEATURES = False
PRINT_PARAMETERS = True

CLEAN_TEXT = True
USE_REFINED_TRAINING = True
NUM_FEATURES = 1000
CONFIDENCE_THRESHOLD = 0.7
USE_STOP_WORDS = False # Only works if CLEAN_TEXT = True
REGULARIZATION = 'l2'

RUN_VALIDATION_SET = True
RUN_TEST_SET = False

PREDICT = False
LOC_PRED_DB = 'data/refined_predicted_data.db'

if USE_STOP_WORDS:
	stop_words = ['climate', 'change', 'climatechange', 'global', 'warming', 'globalwarming']
	stop_words = set(stop_words)
else:
	stop_words = set()

# Logger
class Logger(object):
	def __init__(self):
		self.terminal = sys.stdout
		self.log = open(LOC_LOG, 'a')
	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
	def flush(self):
		pass
if LOG_ENABLED:
	sys.stdout = Logger()

if PRINT_PARAMETERS:
	print("PARAMETERS")
	print("----------")
	print("Clean text? " + str(CLEAN_TEXT))
	print("Refined training data? " + str(USE_REFINED_TRAINING))
	print("Num of Features: " + str(NUM_FEATURES))
	print("Confidence threshold for probability mask: " + str(CONFIDENCE_THRESHOLD))
	print("Use stop words? " + str(USE_STOP_WORDS))
	print("Regularization: " + str(REGULARIZATION))
	print("----------\n")

print("Loading data\n----------")

conn = sqlite3.connect(LOC_TRAIN_DB)
c = conn.cursor()
if USE_REFINED_TRAINING:
	c.execute("SELECT * FROM refined_training")
else:
	c.execute("SELECT * FROM training")
tr_d = c.fetchall()
c.execute("SELECT * FROM test")
te_d = c.fetchall()
c.execute("SELECT * FROM validation")
va_d = c.fetchall()

tr_x = [d[0] for d in tr_d]
tr_y_ = [d[2] for d in tr_d]
te_x = [d[0] for d in te_d]
te_y_ = [d[2] for d in te_d]
va_x = [d[0] for d in va_d]
va_y_ = [d[2] for d in va_d]

print("Done.\n")

if CLEAN_TEXT:
	print("Cleaning data\n----------")
	ptr_x = [process_text(x, stop_words) for x in tr_x]
	pte_x = [process_text(x, stop_words) for x in te_x]
	pva_x = [process_text(x, stop_words) for x in va_x]
	print("Done.\n")
else:
	ptr_x = tr_x
	pte_x = te_x
	pva_x = va_x


# Transform text to document-term matrix
print("Creating document-term matrix\n---------")
cv = CountVectorizer()
cv = cv.fit(ptr_x)
tr_dtmat = cv.transform(ptr_x)
print("Done.\n")

# Feature selection
print("Selecting features\n---------")
sel = SelectKBest(chi2,k=NUM_FEATURES)
tr_dtmat = sel.fit_transform(tr_dtmat,tr_y_)
print("Done.\n")

if PRINT_FEATURES:
	feature_list = cv.get_feature_names()
	feature_map = sel.get_support()
	features = [i for i,j in zip(feature_list, feature_map) if j == True]
	print("Features: " + ','.join(features))

# Train Classifier
print("Training classifier\n---------")
if REGULARIZATION == 'l2':
	clf = LinearSVC(penalty='l2')
else:
	clf = LinearSVC()
clf = CalibratedClassifierCV(clf)
clf.fit(tr_dtmat,tr_y_)
print("Done.\n")

if RUN_VALIDATION_SET:
	print("Running validation set\n---------")
	va_dtmat = cv.transform(pva_x)
	va_dtmat = sel.transform(va_dtmat)
	predicted = clf.predict(va_dtmat)

	probs = clf.predict_proba(va_dtmat)
	prob_mask = []
	for i in range(len(probs)):
		prob = max(probs[i])
		if prob > CONFIDENCE_THRESHOLD:
			prob_mask.append(True)
		else:
			prob_mask.append(False)

	masked_pred = [i for i,j in zip(predicted, prob_mask) if j ==True]
	masked_actual = [i for i,j in zip(va_y_, prob_mask) if j == True]

	num_correct = sum([1 for i,j in zip(masked_pred, masked_actual) if i == j])
	total = len(masked_pred)

	masked_acc = 100.0 * num_correct / total
	print("Masked Accuracy: " + str(masked_acc))
	print("Number of items kept: " + str(total))

	if PRINT_CONFUSION_MATRIX:
		mat = np.zeros((3,3), dtype=int)
		preds = ['a', 's', 'n']
		acts = ['a', 's', 'n']
		for pred,act in zip(masked_pred,masked_actual):
			for i,actual in enumerate(acts):
				for j,predict in enumerate(preds):
					if pred == predict and act == actual:
						mat[i,j] += 1
		print(mat)

	va_acc = 100.0 * clf.score(va_dtmat, va_y_)
	print("Validation Accuracy: " + str(va_acc))

	if PRINT_FULL_RESULTS:
		for i,j,k in zip(predicted,va_y_, pva_x):
			to_print = "Predicted " + i
			to_print += " Actual " + j
			to_print += " Text: " + k
			print(to_print)

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
	print("Done.\n")

if RUN_TEST_SET:
	print("Running test set\n---------")
	te_dtmat = cv.transform(pte_x)
	te_dtmat = sel.transform(te_dtmat)
	predicted = clf.predict(te_dtmat)

	probs = clf.predict_proba(te_dtmat)
	prob_mask = []
	for i in range(len(probs)):
		prob = max(probs[i])
		if prob > CONFIDENCE_THRESHOLD:
			prob_mask.append(True)
		else:
			prob_mask.append(False)

	masked_pred = [i for i,j in zip(predicted, prob_mask) if j ==True]
	masked_actual = [i for i,j in zip(te_y_, prob_mask) if j == True]

	num_correct = sum([1 for i,j in zip(masked_pred, masked_actual) if i == j])
	total = len(masked_pred)

	masked_acc = 100.0 * num_correct / total
	print("Masked Accuracy: " + str(masked_acc))
	print("Number of items kept: " + str(total))

	if PRINT_CONFUSION_MATRIX:
		mat = np.zeros((3,3), dtype=int)
		preds = ['a', 's', 'n']
		acts = ['a', 's', 'n']
		for pred,act in zip(masked_pred,masked_actual):
			for i,actual in enumerate(acts):
				for j,predict in enumerate(preds):
					if pred == predict and act == actual:
						mat[i,j] += 1
		print(mat)

	te_acc = 100.0 * clf.score(te_dtmat, te_y_)
	print("Accuracy: " + str(te_acc))

	if PRINT_FULL_RESULTS:
		for i,j,k in zip(predicted,te_y_, pte_x):
			to_print = "Predicted " + i
			to_print += " Actual " + j
			to_print += " Text: " + k
			print(to_print)

	if PRINT_CONFUSION_MATRIX:
		mat = np.zeros((3,3), dtype=int)
		preds = ['a', 's', 'n']
		acts = ['a', 's', 'n']
		for pred,act in zip(predicted,te_y_):
			for i,actual in enumerate(acts):
				for j,predict in enumerate(preds):
					if pred == predict and act == actual:
						mat[i,j] += 1
		print(mat)
	print("Done.\n")
