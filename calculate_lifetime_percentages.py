import datetime
import matplotlib.pyplot as plt
import numpy as np

import pdb

coverage = int(raw_input("What % of data should be covered? (ex: 90) "))
coverage = 1.0 * coverage

f = open('data/lifetime_data.txt')

ske_lt = {}
act_lt = {}

linenum = 1

for line in f:
	lt = 0
	if len(line.split(' ::---:: ')) == 4:
		text,lt,rt,sent = line.split(' ::---:: ')
		lt = int(round(float(lt) / 3600))
		#print(sent.strip())
		if 'a' in sent:
			act_lt[lt] = act_lt.get(lt,0) + 1
		else:
			ske_lt[lt] = ske_lt.get(lt,0) + 1
	print(str(linenum) + ": " + str(lt))
	linenum += 1
f.close()

X_axis = np.arange(1,100)
Y_act_lt = [act_lt.get(key,0) for key in X_axis]
Y_act_lt = [y*100.0/sum(Y_act_lt) for y in Y_act_lt] # rescale
Y_ske_lt = [ske_lt.get(key,0) for key in X_axis]
Y_ske_lt = [y*100.0/sum(Y_ske_lt) for y in Y_ske_lt] # rescale

act_sum = 0.0
a_hours = 0
while act_sum < coverage:
	act_sum += Y_act_lt[a_hours]
	a_hours += 1
ske_sum = 0.0
s_hours = 0
while ske_sum < coverage:
	ske_sum += Y_ske_lt[s_hours]
	s_hours += 1
print("After " + str(a_hours) + " hours, " + str(act_sum) + "% of activist tweets have exhausted their lifetime.")
print("After " + str(s_hours) + " hours, " + str(ske_sum) + "% of skeptical tweets have exhausted their lifetime.")
