import datetime
import matplotlib.pyplot as plt
import numpy as np

import pdb

f = open('data/switcher_earthday.txt')
lines = f.readlines()
f.close()

activist_changes_3 = {}
skeptical_changes_3 = {}
activist_changes_5 = {}
skeptical_changes_5 = {}
activist_changes_more = {}
skeptical_changes_more = {}

for line in lines:
	if len(line.strip("\n").split(" ", 1)) == 2:
		username,sentiments = line.strip("\n").split(" ", 1)
		sentiments = sentiments.split(" ")
		orig_sent = sentiments[0]
		cur_index = 0
		fut_index = 1
		num_changes = 0
		while fut_index < len(sentiments):
			if sentiments[cur_index] != sentiments[fut_index]:
				num_changes += 1
			cur_index += 1
			fut_index += 1
	#print(username + ":  " + str(num_changes) + " changes with " + str(len(sentiments)) + " tweets.")
	#print(orig_sent)
		if orig_sent == 'a' and len(sentiments) < 3:
			activist_changes_3[num_changes] = activist_changes_3.get(num_changes,0) + 1
		elif orig_sent == 'a' and len(sentiments) < 6:
			activist_changes_5[num_changes] = activist_changes_5.get(num_changes,0) + 1
		elif orig_sent == 'a':
			activist_changes_more[num_changes] = activist_changes_more.get(num_changes,0) + 1
		elif orig_sent == 's' and len(sentiments) < 3:
			skeptical_changes_3[num_changes] = skeptical_changes_3.get(num_changes,0) + 1
		elif orig_sent == 's' and len(sentiments) < 6:
			skeptical_changes_5[num_changes] = skeptical_changes_5.get(num_changes,0) + 1
		else:
			skeptical_changes_more[num_changes] = skeptical_changes_more.get(num_changes,0) + 1

X_axis = np.arange(0,11)

Y_act_3 = [activist_changes_3.get(key,0) for key in X_axis]
Y_act_5 = [activist_changes_5.get(key,0) for key in X_axis]
Y_act_more = [activist_changes_more.get(key,0) for key in X_axis]

Y_ske_3 = [skeptical_changes_3.get(key,0) for key in X_axis]
Y_ske_5 = [skeptical_changes_5.get(key,0) for key in X_axis]
Y_ske_more = [skeptical_changes_more.get(key,0) for key in X_axis]
# Scale
dist_act = [sum(Y_act_3), sum(Y_act_5), sum(Y_act_more)]
Y_act_3 = [y*100.0/sum(Y_act_3) for y in Y_act_3]
Y_act_5 = [y*100.0/sum(Y_act_5) for y in Y_act_5]
Y_act_more = [y*100.0/sum(Y_act_more) for y in Y_act_more]

dist_ske = [sum(Y_ske_3), sum(Y_ske_5), sum(Y_ske_more)]
Y_ske_3 = [y*100.0/sum(Y_ske_3) for y in Y_ske_3]
Y_ske_5 = [y*100.0/sum(Y_ske_5) for y in Y_ske_5]
Y_ske_more = [y*100.0/sum(Y_ske_more) for y in Y_ske_more]

fig = plt.figure()

ax1 = fig.add_subplot(221)
width = 0.3
rects1 = ax1.bar(X_axis, Y_act_3, width, color='yellowgreen')
rects2 = ax1.bar(X_axis+width, Y_act_5, width, color='lightskyblue')
rects3 = ax1.bar(X_axis+width*2, Y_act_more, width, color='lightcoral')
ax1.set_autoscale_on(False)
ax1.axis([0,10,0,100])
ax1.set_title('Activist switches')
ax1.set_ylabel('% of population')
ax1.set_xticks(X_axis + 1.5*width)
ax1.set_xticklabels(X_axis)

ax2 = fig.add_subplot(222)
labels = ['2 tweets', '3-5 tweets', '6+ tweets']
colors = ['yellowgreen','lightskyblue','lightcoral']
ax2.pie(dist_act,labels=labels,colors=colors,shadow=True,autopct='%1.1f%%')
ax2.axis('equal')

ax3 = fig.add_subplot(223)
width = 0.3
rects1 = ax3.bar(X_axis, Y_ske_3, width, color='yellowgreen')
rects2 = ax3.bar(X_axis+width, Y_ske_5, width, color='lightskyblue')
rects3 = ax3.bar(X_axis+width*2, Y_ske_more, width, color='lightcoral')
ax3.set_autoscale_on(False)
ax3.axis([0,10,0,100])
ax3.set_title('Skeptical switches')
ax3.set_ylabel('% of population')
ax3.set_xlabel('# of changes')
ax3.set_xticks(X_axis + 1.5*width)
ax3.set_xticklabels(X_axis)

ax4 = fig.add_subplot(224)
ax4.pie(dist_ske,labels=labels,colors=colors,shadow=True,autopct='%1.1f%%')
ax4.axis('equal')

plt.show()
