import pdb
import sqlite3
import operator
import math
import numpy as np

import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer

from text_processor import process_text

def word2vec(texts,features):
	mat = []
	for text in texts:
		vec = []
		text_set = set(text.split(' '))
		for word in features:
			if word in text_set:
				vec.append(1)
			else:
				vec.append(0)
		mat.append(vec)
	return mat

def sent2onehot(sent):
	if sent == 'a':
		return [1, 0, 0]
	if sent == 's':
		return [0, 1, 0]
	if sent == 'n':
		return [0, 0, 1]

DATA_LOC = './tf_data'
ETA = 0.001

stop_words = set()

#Load Data
conn = sqlite3.connect('data/refined_training_data.db')
c = conn.cursor()
c.execute("SELECT * FROM training")
tr_d = c.fetchall()
c.execute("SELECT * FROM test")
te_d = c.fetchall()
c.execute("SELECT * FROM validation")
va_d = c.fetchall()

tr_x = [d[0] for d in tr_d]
tr_y_ = [sent2onehot(d[2]) for d in tr_d]
te_x = [d[0] for d in te_d]
te_y_ = [sent2onehot(d[2]) for d in te_d]
va_x = [d[0] for d in va_d]
va_y_ = [sent2onehot(d[2]) for d in va_d]

ptr_x = [process_text(x, stop_words) for x in tr_x]
pte_x = [process_text(x, stop_words) for x in te_x]
pva_x = [process_text(x, stop_words) for x in va_x]

vocab_size = 1000
vocab = {}

for text in ptr_x:
	tokens = text.split(' ')
	for t in tokens:
		vocab[t] = vocab.get(t, 0) + 1
sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)[:vocab_size]
features = [v[0] for v in sorted_vocab]

tr_dtmat = word2vec(ptr_x, features)
va_dtmat = word2vec(pva_x, features)

x = tf.placeholder(tf.float32, [None,1000], name='x-input')
y_ = tf.placeholder(tf.float32, [None,3], name='y-input')

with tf.name_scope('hidden1'):
	sigma1 = 1.0 / math.sqrt(float(1000))
	Wh = tf.Variable(tf.truncated_normal([1000,30],stddev=sigma1),name='weights')
	bh = tf.Variable(tf.zeros([30]), name='biases')
	hidden1 = tf.nn.relu(tf.matmul(x,Wh) + bh)
with tf.name_scope('softmax'):
	sigma2 = 1.0 / math.sqrt(30)
	Ws = tf.Variable(tf.truncated_normal([30,3], stddev=sigma2), name='weights')
	bs = tf.Variable(tf.zeros([3]), name='biases')
	net = tf.matmul(hidden1,Ws) + bs
	prob_dist = tf.nn.softmax(net, name='prob_dist')
	prediction = tf.nn.top_k(prob_dist, 1)

with tf.name_scope('Loss'):
	c_e = tf.nn.softmax_cross_entropy_with_logits(net, y_, name='cross_entropy')
	loss = tf.reduce_mean(c_e, name='xentropy_mean')

with tf.name_scope('Backprop'):
	opt = tf.train.GradientDescentOptimizer(ETA)
	grads = opt.compute_gradients(loss)
	apply_gradient_op = opt.apply_gradients(grads)


sess = tf.Session()
sess.run(tf.initialize_all_variables())

for i in range(0,5900, 10):
	_, cur_loss = sess.run((apply_gradient_op, loss), feed_dict={
		x: tr_dtmat[i:i+100],
		y_: tr_y_[i:i+100]
	})
	print(cur_loss)

	probs = sess.run((prob_dist), feed_dict={
		x: va_dtmat,
		y_: va_y_
	})

	max_prob,preds = sess.run((prediction), feed_dict={
		x: va_dtmat,
		y_: va_y_
	})
	#pdb.set_trace()

#pdb.set_trace()
