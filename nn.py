import pdb
import sqlite3

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest,chi2

from nn_models import beginner,CNN

def encoder(labels):
	for i in range(len(labels)):
		if labels[i] == 'a':
			labels[i] = [1,0,0]
		if labels[i] == 's':
			labels[i] = [0,1,0]
		if labels[i] == 'n':
			labels[i] = [0,0,1]
	return labels

# Flags
ETA = 0.1
DATA_LOC = './tf_data'
BATCH_SIZE = 50
NUM_BATCHES = 500

# Load data
conn = sqlite3.connect('data/refined_training_data.db')
c = conn.cursor()
c.execute("SELECT * FROM training")
tr_d = c.fetchall()
c.execute("SELECT * FROM test")
te_d = c.fetchall()
c.execute("SELECT * FROM validation")
va_d = c.fetchall()
conn.close()

tr_a = [d for d in tr_d if d[2] == 'a']
tr_s = [d for d in tr_d if d[2] == 's']
tr_o = [d for d in tr_d if d[2] == 'n']

#tr_d = np.concatenate((tr_a[:800],tr_s,tr_o[:800]),axis=0)

tr_x = [d[0] for d in tr_d]
tr_y_ = [d[2] for d in tr_d]
va_x = [d[0] for d in va_d]
va_y_ = [d[2] for d in va_d]

# Build word vectorizer using scikit-learn
cv = CountVectorizer(stop_words=['global', 'warming', 'globalwarming', 'climate', 'change', 'climatechange', 'http', 'https'])
cv = cv.fit(tr_x)
tr_dtmat = cv.transform(tr_x)
sel = SelectKBest(chi2,k=100)
sel.fit(tr_dtmat,tr_y_)

# CREATE GRAPH

# Input nodes
with tf.name_scope('Inputs'):
	x = tf.placeholder(tf.float32, [None, 100], name='x_input')
	y_ = tf.placeholder(tf.float32, [None, 3], name='y_input')

# Model nodes
with tf.name_scope('CNN'):
	net, var_dict = beginner(x)
#	net, var_dict = CNN(x)
	y = tf.identity(net)
#y = tf.nn.softmax(net, name='predicted_y')
#pdb.set_trace()

# Loss nodes
with tf.name_scope('Loss'):
	cross_entropy = tf.nn.softmax_cross_entropy_with_logits(y, y_, name='cross_entropy')
	loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
	tf.scalar_summary(loss.op.name, loss)

# Training nodes
# opt = optimizer
# op = operation
with tf.name_scope('Backprop'):
	opt = tf.train.GradientDescentOptimizer(ETA)
	grads = opt.compute_gradients(loss)
	step = tf.Variable(0, name='train_step_num', trainable=False)
	apply_gradient_op = opt.apply_gradients(grads, global_step=step)
#	cnn_train_op = cnn_opt.minimize(loss, global_step=step)

for var in tf.trainable_variables():
	tf.histogram_summary(var.op.name, var)

for grad, var in grads:
	if grad is not None:
		tf.histogram_summary(var.op.name + '/gradients', grad)

# Eval nodes
_,y_prime = tf.nn.top_k(y_, 1)
y_prime = tf.reshape(y_prime,[-1])
correct = tf.nn.in_top_k(y, y_prime, 1)
eval_op = tf.reduce_sum(tf.cast(correct, tf.int32))

def do_eval(sess, eval_op):
	num_eval = 10
	data_set = (sel.transform(cv.transform(va_x[:10])).toarray(), encoder(va_y_[:10]))
	result,true_count = sess.run((y,eval_op), feed_dict={
		x: data_set[0].reshape((num_eval,100)),
		y_: data_set[1],
	})
	print(result)
	print(data_set[1])
	pdb.set_trace()
        precision = 100.0 * true_count / num_eval
        print(' Num examples: %d Num correct: %d Precision: %0.04f' % (num_eval, true_count, precision))

# SCRIPT START
summary_op = tf.merge_all_summaries()

sess = tf.Session()
summary_writer = tf.train.SummaryWriter(DATA_LOC, sess.graph)
sess.run(tf.initialize_all_variables())


saver = tf.train.Saver(var_dict)
for i in range(NUM_BATCHES):
#	np.random.shuffle(tr_d)
	batch = tr_d[:BATCH_SIZE]
	batch_x = [d[0] for d in batch]
	batch_y = encoder([d[2] for d in batch])
	batch_x = sel.transform(cv.transform(batch_x)).toarray()
#	pdb.set_trace()
	_,cur_loss, summary_str = sess.run((apply_gradient_op, loss, summary_op), feed_dict={
		x: batch_x,
		y_: batch_y
	})

        summary_writer.add_summary(summary_str, i)
        summary_writer.flush()

#	test = sess.run(y, feed_dict={
#		x: batch[0],
#		y_: batch[1]
#	})
#	pdb.set_trace()
	do_eval(sess, eval_op)
	print('Training batch #{} of {}'.format(i,NUM_BATCHES) + " loss: " + str(cur_loss))
#saver.save(sess, DATA_LOC + '/CNN.ckpt')
pdb.set_trace()
