import datetime
import matplotlib.pyplot as plt
import numpy as np

import pdb

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

pdb.set_trace()

fig = plt.figure()
ax1 = fig.add_subplot(111)
width = 0.4 
rects1 = ax1.bar(X_axis, Y_act_lt, width, color='yellowgreen', edgecolor="none")
rects2 = ax1.bar(X_axis+width, Y_ske_lt, width, color='lightskyblue', edgecolor="none")
#ax1.set_title('Lifetime Distribution')
ax1.set_ylabel('Percent of population')
ax1.set_xlabel('Lifetime (hours)')
ax1.legend((rects1[0],rects2[0]), ('Activists', 'Skeptics'))

plt.savefig("analysis/lifetime.eps", format="eps")
plt.show()
