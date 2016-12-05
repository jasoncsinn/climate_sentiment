import numpy as np
import sqlite3
import matplotlib.pyplot as plt

from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest,chi2
from sklearn.calibration import CalibratedClassifierCV

from util import get_time_mask,load_lines_from_file,can_parse,parse_tweet,process_text

import pdb
import sys
import operator

LOC_TRAIN_DB = 'data/refined_training_data.db'
LOC_LOG = 'data/ambiguity.log'
LOG_ENABLED = True
PRINT_FEATURES = False
PRINT_PARAMETERS = True

CLEAN_TEXT = True
USE_REFINED_TRAINING = True
NUM_FEATURES = 'all'
USE_STOP_WORDS = False # Only works if CLEAN_TEXT = True
REGULARIZATION = 'l2'

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
c.execute("SELECT * FROM validation WHERE sent='a'")
va_d = c.fetchall()

tr_x = [d[0] for d in tr_d]
tr_y_ = [d[2] for d in tr_d]
va_x = [d[0] for d in va_d]
va_y_ = [d[2] for d in va_d]

print("Done.\n")

if CLEAN_TEXT:
	print("Cleaning data\n----------")
	ptr_x = [process_text(x, stop_words) for x in tr_x]
	pva_x = [process_text(x, stop_words) for x in va_x]
	print("Done.\n")
else:
	ptr_x = tr_x
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

feature_list = cv.get_feature_names()
feature_map = sel.get_support()
features = [i for i,j in zip(feature_list, feature_map) if j == True]
if PRINT_FEATURES:
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

print("Running validation set\n----------")
va_dtmat = cv.transform(pva_x)
va_dtmat = sel.transform(va_dtmat)
probs = clf.predict_proba(va_dtmat)
for line,dist in zip(pva_x, probs):
	dist = [str(p) for p in dist]
	print(line + ' ' + ' '.join(dist))
acc = clf.score(va_dtmat, va_y_)
print(str(acc))

# Find word ambiguities
#test = cv.transform([""])
#test = sel.transform(test)
#probs = clf.predict_proba(test)

#pdb.set_trace()

word_dtmat = cv.transform(features)
word_dtmat = sel.transform(word_dtmat)

probs = clf.predict_proba(word_dtmat)

entropies = []
for dist in probs:
	entropy = 0
	for prob in dist:
		entropy -= prob * np.log(prob)
	entropies.append(entropy)

ent_ht = {}
for i,j in enumerate(entropies):
	ent_ht[i] = j

# Find word frequencies
word_freq_mat = np.transpose(tr_dtmat.toarray())
word_freqs = [sum(column) for column in word_freq_mat]

#pdb.set_trace()

# Make entropy mask to sort by ambiguity
sorted_pairs = sorted(ent_ht.items(), key=operator.itemgetter(1))
mask = [p[0] for p in sorted_pairs]

ordered_probs = [probs[i] for i in mask]
ordered_ents = [entropies[i] for i in mask]
ordered_features = [feature_list[i] for i in mask]
ordered_word_freqs = [word_freqs[i] for i in mask]

with open('analysis/word_ambiguities.txt', 'w') as f:
	for i,j,k,l in zip(ordered_probs, ordered_ents, ordered_features, ordered_word_freqs):
		i = [str(i[0] - 0.20433224), str(i[1] - 0.60818274), str(i[2] - 0.12748502)]
		to_write = 'Probabilities: ' + ' '.join(i)
		to_write += ' Entropy: ' + str(j)
		to_write += ' Word: ' + k
		to_write += ' Freq: ' + str(l)
		to_write += '\n'
		f.write(to_write)

pdb.set_trace()
