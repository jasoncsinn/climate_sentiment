import numpy as np
import sqlite3
import matplotlib.pyplot as plt

from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest,chi2
from sklearn.calibration import CalibratedClassifierCV

from util import get_time_mask,load_lines_from_file,can_parse,parse_tweet,process_text

import pdb
import sys

LOC_TRAIN_DB = 'data/refined_training_data.db'
LOC_LOG = 'data/svm.log'
LOG_ENABLED = True
PRINT_FULL_RESULTS = False
PRINT_CONFUSION_MATRIX = True
PRINT_FEATURES = False
PRINT_PARAMETERS = True

CLEAN_TEXT = True
USE_REFINED_TRAINING = True
TF_IDF = True
NUM_FEATURES = 740
CONFIDENCE_THRESHOLD = 0.7
USE_STOP_WORDS = False # Only works if CLEAN_TEXT = True
REGULARIZATION = 'l2'

RUN_VALIDATION_SET = True
RUN_TEST_SET = True

PREDICT = False
FILTER_PREDICTIONS = False
CONTINUOUS = True
LOC_PRED_DB = 'data/predicted_data.db'
table_names,_ = get_time_mask()
PRED_BATCH_SIZE = 10000
blacklist = []

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
cv = CountVectorizer(min_df=2)
cv = cv.fit(ptr_x)
tr_dtmat = cv.transform(ptr_x)
if TF_IDF:
	tfidf = TfidfTransformer()
	tr_dtmat = tfidf.fit_transform(tr_dtmat)
print("Done.\n")

# Feature selection
print("Selecting features\n---------")
sel = SelectKBest(chi2,k=NUM_FEATURES)
tr_dtmat = sel.fit_transform(tr_dtmat,tr_y_)
print("Done.\n")

if TF_IDF:
	print("Implementing tf-idf\n----------")
	tfidf = TfidfTransformer(use_idf=False)
	tr_dtmat = tfidf.fit_transform(tr_dtmat)
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
	if TF_IDF:
		va_dtmat = tfidf.transform(va_dtmat)
	predicted = clf.predict(va_dtmat)

	# Create probability mask
	probs = clf.predict_proba(va_dtmat)
	confidences = []
	prob_mask = []
	for i in range(len(probs)):
		prob = max(probs[i])
		confidences.append(prob)
		if prob > CONFIDENCE_THRESHOLD:
			prob_mask.append(True)
		else:
			prob_mask.append(False)

	# Apply probability mask
	masked_pred = [i for i,j in zip(predicted, prob_mask) if j ==True]
	masked_actual = [i for i,j in zip(va_y_, prob_mask) if j == True]

	# Statistics
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
		for i,j,k,l in zip(predicted,va_y_, pva_x, confidences):
			to_print = "Predicted " + i
			to_print += " Actual " + j
			to_print += " Confidence: " + str(l)
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
	if TF_IDF:
		te_dtmat = tfidf.transform(te_dtmat)
	predicted = clf.predict(te_dtmat)

	# Create probability mask
	probs = clf.predict_proba(te_dtmat)
	prob_mask = []
	confidences = []
	for i in range(len(probs)):
		prob = max(probs[i])
		confidences.append(prob)
		if prob > CONFIDENCE_THRESHOLD:
			prob_mask.append(True)
		else:
			prob_mask.append(False)

	# Apply probability mask
	masked_pred = [i for i,j in zip(predicted, prob_mask) if j ==True]
	masked_actual = [i for i,j in zip(te_y_, prob_mask) if j == True]

	# Statistics
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
		for i,j,k,l in zip(predicted,te_y_, pte_x,confidences):
			to_print = "Predicted " + i
			to_print += " Actual " + j
			to_print += " Confidence: " + str(l)
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


if PREDICT:
	print("Prediction Phase\n----------")
	with sqlite3.connect(LOC_PRED_DB) as pred_conn:
		pred_c = pred_conn.cursor()

		for table_name in table_names[:]:
			cur_line = 1
			fn = 'data/full_tweet_data/' + table_name + '.txt'
			tweets = load_lines_from_file(fn, PRED_BATCH_SIZE, cur_line)
			while len(tweets) > 0:
				print('Inferring sentiment with tweet # ' + str(cur_line) + ' from ' + table_name)
				# Build data
				texts = []
				dates = []
				usernames = []
				locations = []
				for tweet_str in tweets:
					if can_parse(tweet_str, blacklist):
						date, text, username, location = parse_tweet(tweet_str)
						dates.append(date)
						texts.append(text)
						usernames.append(username)
						locations.append(location)
				# Infer data
				ppred_x = [process_text(x, stop_words) for x in texts]
				pred_dtmat = cv.transform(ppred_x)
				pred_dtmat = sel.transform(pred_dtmat)
				pred_predictions = clf.predict(pred_dtmat)

				if CONTINUOUS:
					# Build probability mask and calculate entropy
					pred_probs = clf.predict_proba(pred_dtmat)
					entropies = []
					for dist in pred_probs:
						entropy = 0
						for prob in dist:
							entropy -= prob * np.log(prob)
						entropies.append(entropy)

					prob_mask = []
					for i in range(len(pred_probs)):
						prob = max(pred_probs[i])
						if prob > CONFIDENCE_THRESHOLD:
							prob_mask.append(True)
						else:
							prob_mask.append(False)

					# Apply probability mask
					if FILTER_PREDICTIONS:
						m_dates = [i for i,j in zip(dates, prob_mask) if j == True]
						m_texts = [i for i,j in zip(texts, prob_mask) if j == True]
						m_usernames = [i for i,j in zip(usernames, prob_mask) if j == True]
						m_locations = [i for i,j in zip(locations, prob_mask) if j == True]
						m_sents = [i for i,j in zip(pred_predictions, prob_mask) if j == True]
					else:
						m_dates = dates
						m_texts = texts
						m_usernames = usernames
						m_locations = locations
						m_sents = []
						for i in range(len(prob_mask)):
							if prob_mask[i] == False:
								m_sents.append('u')
							else:
								m_sents.append(pred_predictions[i])

					# Insert into database
					for i in range(len(m_dates)):
						to_execute = "INSERT INTO " + table_name + " VALUES (\'"
	#					to_execute = "INSERT INTO full_tweets VALUES(\'"
						to_execute += m_texts[i] + "\',\'"
						to_execute += m_dates[i] + "\',\'"
						to_execute += m_usernames[i] + "\',\'"
						to_execute += m_locations[i] + "\',\'"
						to_execute += m_sents[i] + "\',\'"
						to_execute += str(entropies[i]) + "\')"
						pred_c.execute(to_execute)
					cur_line += PRED_BATCH_SIZE
					tweets = load_lines_from_file(fn, PRED_BATCH_SIZE, cur_line)
				# DISCRETE MODE
				else:
					for i in range(len(dates)):
						to_execute = "INSERT INTO " + table_name + " VALUES(\'"
						to_execute += texts[i] + "\',\'"
						to_execute += dates[i] + "\',\'"
						to_execute += usernames[i] + "\',\'"
						to_execute += locations[i] + "\',\'"
						to_execute += pred_predictions[i] + "\')"
						pred_c.execute(to_execute)
					cur_line += PRED_BATCH_SIZE
					tweets = load_lines_from_file(fn, PRED_BATCH_SIZE, cur_line)
				# DISCRETE MODE
	print("Done.")
