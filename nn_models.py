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

def lenet(images):
    """
    Lenet model.

    Expected input shape: None, 784
    """
    images = tf.reshape(images, [-1, 28, 28, 1])  # let tf guess the first dimension
    net = slim.layers.conv2d(images, 20, [5,5], scope='conv1')
    net = slim.layers.max_pool2d(net, [2,2], scope='pool1')
    net = slim.layers.conv2d(net, 50, [5,5], scope='conv2')
    net = slim.layers.max_pool2d(net, [2,2], scope='pool2')
    net = slim.layers.flatten(net, scope='flatten3')
    net = slim.layers.fully_connected(net, 500, scope='fully_connected4')
    net = slim.layers.fully_connected(net, 10, activation_fn=None, scope='fully_connected5')

    L0_vars = tf.get_collection(tf.GraphKeys.VARIABLES, scope='conv1')
    L1_vars = tf.get_collection(tf.GraphKeys.VARIABLES, scope='pool1')
    L2_vars = tf.get_collection(tf.GraphKeys.VARIABLES, scope='conv2')
    L3_vars = tf.get_collection(tf.GraphKeys.VARIABLES, scope='pool2')
    L4_vars = tf.get_collection(tf.GraphKeys.VARIABLES, scope='flatten3')
    L5_vars = tf.get_collection(tf.GraphKeys.VARIABLES, scope='fully_connected4')
    L6_vars = tf.get_collection(tf.GraphKeys.VARIABLES, scope='fully_connected5')
    var_dict = {
        'C1W': L0_vars[0],
        'C1b': L0_vars[1],
        'C2W': L2_vars[0],
        'C2b': L2_vars[1],
        'FC4W': L5_vars[0],
        'FC4b': L5_vars[1],
        'FC5W': L6_vars[0],
        'FC5b': L6_vars[1],
    }
    return net, var_dict
