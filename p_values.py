import pdb
import numpy as np

from random import shuffle
from scipy.stats import wilcoxon

events = ['cop21', 'dicaprio', 'earthday', 'trump']

for event in events:
	pre_a = []
	post_a = []
	pre_s = []
	post_s = []
	pre_n = []
	post_n = []
	with open('data/tsr_' + event + '/pre_data.txt') as f:
		for line in f:
			line = line.strip('\n').split(' ::---:: ')
			if len(line) == 6:
				_, _, _, _, sent, ent = line
				ent = float(ent)
				if sent == 'a':
					pre_a.append(ent)
				elif sent == 's':
					pre_s.append(ent)
				elif sent == 'n':
					pre_n.append(ent)

	with open('data/tsr_' + event + '/post_data.txt') as f:
		for line in f:
			line = line.strip('\n').split(' ::---:: ')
			if len(line) == 6:
				_, _, _, _, sent, ent = line
				ent = float(ent)
				if sent == 'a':
					post_a.append(ent)
				elif sent == 's':
					post_s.append(ent)
				elif sent == 'n':
					post_n.append(ent)
	print(str(len(pre_a)) +' '+ str(len(pre_s)) +' '+ str(len(pre_n)))
	print(str(len(post_a)) +' '+ str(len(post_s)) +' '+ str(len(post_n)))
#	pdb.set_trace()

	shuffle(pre_a)
	shuffle(post_a)
	pre_a = pre_a[:10000]
	post_a = post_a[:10000]

	shuffle(pre_s)
	shuffle(post_s)
	pre_s = pre_s[:10000]
	post_s = post_s[:10000]

	shuffle(pre_n)
	shuffle(post_n)
	pre_n = pre_n[:10000]
	post_n = post_n[:10000]

	_,pv_a = wilcoxon(pre_a, post_a)
	_,pv_s = wilcoxon(pre_s, post_s)
	_,pv_n = wilcoxon(pre_n, post_n)

	pdb.set_trace()
	
	print("Event: " + event)
	print("pvalue a: " + str(pv_a))
	print("pvalue s: " + str(pv_s))
	print("pvalue n: " + str(pv_n))
	print('\n')

