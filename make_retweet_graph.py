import datetime
import matplotlib.pyplot as plt
import numpy as np

import pdb

f = open('data/lifetime_data.txt')

ske_rt = {}
act_rt = {}

linenum = 1

for line in f:
	if len(line.split(' ::---:: ')) == 4:
		text,lt,rt,sent = line.split(' ::---:: ')
		rt = int(rt)
	#print(sent.strip())
		if 'a' in sent:
			act_rt[rt] = act_rt.get(rt,0) + 1
		else:
			ske_rt[rt] = ske_rt.get(rt,0) + 1
	print(str(linenum))
	linenum += 1
f.close()

X_axis = np.arange(2,50)
Y_act_rt = [act_rt.get(key,0) for key in X_axis]
Y_act_rt = [y*100.0/sum(Y_act_rt) for y in Y_act_rt] # rescale
Y_ske_rt = [ske_rt.get(key,0) for key in X_axis]
Y_ske_rt = [y*100.0/sum(Y_ske_rt) for y in Y_ske_rt] # rescale

#pdb.set_trace()

fig = plt.figure()
ax1 = fig.add_subplot(111)
width = 0.4
rects1 = ax1.bar(X_axis, Y_act_rt, width, color='yellowgreen')
rects2 = ax1.bar(X_axis+width, Y_ske_rt, width, color='lightskyblue')
ax1.set_autoscale_on(False)
ax1.axis([2,50,0,45])
ax1.set_title('Retweet Distribution')
ax1.set_ylabel('% of population')
ax1.set_xlabel('# of retweets (including original)')
ax1.legend((rects1[0],rects2[0]), ('Activists', 'Skeptics'))

plt.show()
