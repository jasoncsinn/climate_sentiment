import datetime
import matplotlib.pyplot as plt
import numpy as np

import pdb

f = open('data/switcher_data.txt')
lines = f.readlines()
f.close()

activist_changes = {}
skeptical_changes = {}

for line in lines:
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
	if orig_sent == 'a':
		activist_changes[num_changes] = activist_changes.get(num_changes,0) + 1
	else:
		skeptical_changes[num_changes] = skeptical_changes.get(num_changes,0) + 1
X_axis = np.arange(0,15)
Y_act = [activist_changes.get(key,0) for key in X_axis]
Y_ske = [skeptical_changes.get(key,0) for key in X_axis]
pdb.set_trace()
fig, ax = plt.subplots()
rects1 = ax.bar(X_axis, Y_act, 0.35, color='g')
rects2 = ax.bar(X_axis+0.35, Y_ske, 0.35, color='r')
ax.legend((rects1[0], rects2[0]), ('Activists', 'Skepticals'))
plt.show()
#pdb.set_trace()
