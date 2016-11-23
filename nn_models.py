import os
import math

import tensorflow as tf
import tensorflow.contrib.slim as slim


# Model format:
def beginner(dtmat):
	x = tf.reshape(dtmat, [-1, 100])
	with tf.name_scope('hidden1'):
        	sigma1 = 1.0 / math.sqrt(float(100))
                Wh = tf.Variable(tf.truncated_normal([100,500],stddev=sigma1),name='weights')
                bh = tf.Variable(tf.zeros([500]),name='biases')
                hidden1 = tf.nn.relu(tf.matmul(x,Wh) + bh)
        with tf.name_scope('softmax'):
                sigma2 = 1.0 / math.sqrt(500)
                Ws = tf.Variable(tf.truncated_normal([500,3],stddev=sigma2),name='weights')
                bs = tf.Variable(tf.zeros([3]),name='biases')
                net = tf.matmul(hidden1,Ws) + bs
	model_var_dict = {
		'Wh': Wh,
		'bh': bh,
		'Ws': Ws,
		'bs': bs,
	}
        return net, model_var_dict

def CNN(images):
	images = tf.reshape(images, [-1, 28, 28, 1])
	with tf.name_scope('conv1'):
		kernel1 = tf.Variable(tf.truncated_normal([5, 5, 1, 64],stddev=5e-2), name='kernel1')
		conv = tf.nn.conv2d(images, kernel1, [1, 1, 1, 1], padding='SAME')
		biases1 = tf.Variable(tf.zeros([64]), name='biases1')
		bias = tf.nn.bias_add(conv, biases1)
		conv1 = tf.nn.relu(bias, name='conv1')
	pool1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool1')
	norm1 = tf.nn.local_response_normalization(pool1, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75, name='norm1')

	with tf.name_scope('conv2'):
		kernel2 = tf.Variable(tf.truncated_normal([5, 5, 64, 64],stddev=5e-2), name='kernel2')
		conv = tf.nn.conv2d(norm1, kernel2, [1, 1, 1, 1], padding='SAME')
		biases2 = tf.Variable(tf.constant(0.1, shape=[64]), name='biases1')
		bias = tf.nn.bias_add(conv, biases2)
		conv2 = tf.nn.relu(bias, name='conv2')
	pool2 = tf.nn.max_pool(conv2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool2')
	norm2 = tf.nn.local_response_normalization(pool2, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75, name='norm2')

	reshape = tf.reshape(norm2, [-1, 3136])
	with tf.name_scope('hidden1'):
                Wh = tf.Variable(tf.truncated_normal([3136, 300],stddev=0.04),name='weights')
                bh = tf.Variable(tf.constant(0.1, shape=[300]),name='biases')
                hidden1 = tf.nn.relu(tf.matmul(reshape,Wh) + bh)
        with tf.name_scope('softmax'):
                sigma2 = 1.0 / 300.0
                Ws = tf.Variable(tf.truncated_normal([300,10],stddev=sigma2),name='weights')
                bs = tf.Variable(tf.zeros([10]),name='biases')
                net = tf.matmul(hidden1,Ws) + bs
	model_var_dict = {
		'kernel1': kernel1,
		'biases1': biases1,
		'kernel2': kernel2,
		'biases2': biases2,
		'Wh': Wh,
		'bh': bh,
		'Ws': Ws,
		'bs': bs
	}
	return net, model_var_dict

