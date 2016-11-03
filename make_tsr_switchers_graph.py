import datetime
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

import pdb
import sys

# Logger
class Logger(object):
	def __init__(self):
		self.terminal = sys.stdout
		self.log = open("data/tsr_bn_khaled/tsr_switcher_stats_bn_khaled.txt", "a")
	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
	def flush(self):
		pass
#sys.stdout = Logger()

s = [0, 0, 0, 0, 0, 0] # [to_a[0], to_n[0], to_a[last], to_n[last], numorig, numfinal]
a = [0, 0, 0, 0, 0, 0]
n = [0, 0, 0, 0, 0, 0]

MODE = "LAST"
TITLE = "Earth Day - Apr 22nd, 2016"

with open('data/tsr_earthday/switcher_earthday.txt') as f:
	for line in f:
		if len(line.strip("\n").split(" ")) > 4:
			username, _, _, pre, post = line.strip('\n').split(" ", 4)
			post = post.split(" ")
			if MODE == "FIRST":
				if post[0] == 'a':
					a[5] += 1
				elif post[0] == 's':
					s[5] += 1
				elif post[0] == 'n':
					n[5] += 1
			else:
				if post[-1] == 'a':
					a[5] += 1
				if post[-1] == 's':
					s[5] += 1
				elif post[-1] == 'n':
					n[5] += 1
			if pre == 's':
				s[4] += 1
				if MODE == "FIRST":
					if post[0] == 'a':
						s[0] += 1
					elif post[0] == 'n':
						s[1] += 1
				else:
					if post[-1] == 'a':
						s[2] += 1
					elif post[-1] == 'n':
						s[3] += 1
			if pre == 'a':
				a[4] += 1
				if MODE == "FIRST":
					if post[0] == 's':
						a[0] += 1
					elif post[0] == 'n':
						a[1] += 1
				else:
					if post[-1] == 's':
						a[2] += 1
					elif post[-1] == 'n':
						a[3] += 1
			if pre == 'n':
				n[4] += 1
				if MODE == "FIRST":
					if post[0] == 'a':
						n[0] += 1
					elif post[0] == 's':
						n[1] += 1
				else:
					if post[-1] == 'a':
						n[2] += 1
					elif post[-1] == 's':
						n[3] += 1

s_normed = [round(i*100.0/s[4], 2) for i in s]
a_normed = [round(i*100.0/a[4], 2) for i in a]
n_normed = [round(i*100.0/n[4], 2) for i in n]

print("MODE: " + MODE)

print("# of pre activists: " + str(a[4]))
print("# of pre skeptics: " + str(s[4]))
print("# of pre others: " + str(n[4]))

print("# of post activists: " + str(a[5]))
print("# of post skeptics: " + str(s[5]))
print("# of post others: " + str(n[5]))

if MODE == "FIRST":
	i = (0,1)
else:
	i = (2,3)

print("Raw nums ")
print("orig=s post=a num: " + str(s[i[0]]))
print("orig=a post=s num: " + str(a[i[0]]))
print("orig=n post=a num: " + str(n[i[0]]))
print("orig=n post=s num: " + str(n[i[1]]))
print("orig=s post=n num: " + str(s[i[1]]))
print("orig=a post=n num: " + str(a[i[1]]))

print("Proportions ")
print("orig=s post=a num: " + str(s_normed[i[0]]))
print("orig=a post=s num: " + str(a_normed[i[0]]))
print("orig=n post=a num: " + str(n_normed[i[0]]))
print("orig=n post=s num: " + str(n_normed[i[1]]))
print("orig=s post=n num: " + str(s_normed[i[1]]))
print("orig=a post=n num: " + str(a_normed[i[1]]))

ax1 = plt.subplot2grid((4,8), (1,0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((4,8), (1,2), colspan=1, rowspan=2)
ax3 = plt.subplot2grid((4,8), (0,3), colspan=5, rowspan=4)
x = np.arange(0,3)
pre = [a[4], s[4], n[4]]
post = [a[5], s[5], n[5]]
labels = ['activists', 'skeptics', 'others']

barlist_pre = ax1.bar(x, pre, 0.4, edgecolor='black')
barlist_post = ax1.bar(x+0.4, post, 0.4, edgecolor='black')

ax1.set_xticks(x+0.4)
ax1.set_xticklabels(labels)
plt.setp(ax1.get_xticklabels(), rotation=90)

barlist_pre[0].set_color('yellowgreen')
barlist_post[0].set_color('green')
barlist_pre[1].set_color('lightcoral')
barlist_post[1].set_color('red')
barlist_pre[2].set_color('lightgray')
barlist_post[2].set_color('gray')

ax1.set_ylabel('# of people')
ax1.set_title('Populations')

percents = [100.0*(a[5] - a[4])/a[4], 100.0*(s[5] - s[4])/s[4], 100.0*(n[5] - n[4])/n[4]]
barlist_percents = ax2.bar(x+0.4, percents, 0.2)

ax2.set_xticks(x + 0.5)
ax2.set_xticklabels(labels)
ax2.set_autoscale_on(False)
ax2.axis([0, 3, -100, 100])
plt.setp(ax2.get_xticklabels(), rotation=90)

barlist_percents[0].set_color('yellowgreen')
barlist_percents[1].set_color('lightcoral')
barlist_percents[2].set_color('lightgray')

#ax2.set_ylabel('% of original population')
ax2.set_title('Net %Change')

#G=nx.dodecahedral_graph()
G = nx.DiGraph()
G.add_node('Activists', pos=(0,0))
G.add_node('Skeptics', pos=(3,3))
G.add_node('Others', pos=(6,0))
G.add_node('Activists2', pos=(0,-6))
G.add_node('Skeptics2', pos=(3,-3))
G.add_node('Others2', pos=(6,-6))
G.add_node('ActivistsP', pos=(9,0))
G.add_node('SkepticsP', pos=(12,3))
G.add_node('OthersP', pos=(15,0))
G.add_node('Activists2P', pos=(9,-6))
G.add_node('Skeptics2P', pos=(12,-3))
G.add_node('Others2P', pos=(15,-6))

G.add_edge('Activists', 'Skeptics', weight=a[i[0]])
G.add_edge('Skeptics', 'Others', weight=s[i[1]])
G.add_edge('Others', 'Activists', weight=n[i[0]])
G.add_edge('Activists2', 'Others2', weight=a[i[1]])
G.add_edge('Skeptics2', 'Activists2', weight=s[i[0]])
G.add_edge('Others2', 'Skeptics2', weight=n[i[1]])
G.add_edge('ActivistsP', 'SkepticsP', weight=a_normed[i[0]])
G.add_edge('SkepticsP', 'OthersP', weight=s_normed[i[1]])
G.add_edge('OthersP', 'ActivistsP', weight=n_normed[i[0]])
G.add_edge('Activists2P', 'Others2P', weight=a_normed[i[1]])
G.add_edge('Skeptics2P', 'Activists2P', weight=s_normed[i[0]])
G.add_edge('Others2P', 'Skeptics2P', weight=n_normed[i[1]])

pos=nx.get_node_attributes(G, 'pos')
nx.draw_networkx_nodes(G, pos, nodelist = ['Activists'], node_color='yellowgreen', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['Skeptics'], node_color='lightcoral', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['Others'], node_color='lightgray', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['Activists2'], node_color='yellowgreen', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['Skeptics2'], node_color='lightcoral', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['Others2'], node_color='lightgray', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['ActivistsP'], node_color='yellowgreen', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['SkepticsP'], node_color='lightcoral', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['OthersP'], node_color='lightgray', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['Activists2P'], node_color='yellowgreen', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['Skeptics2P'], node_color='lightcoral', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist = ['Others2P'], node_color='lightgray', node_size=3000)
nx.draw_networkx_edges(G, pos)

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

node_labels = {}
node_labels['Activists'] = 'Activists'
node_labels['Skeptics'] = 'Skeptics'
node_labels['Others'] = 'Others'
node_labels['Activists2'] = 'Activists'
node_labels['Skeptics2'] = 'Skeptics'
node_labels['Others2'] = 'Others'
node_labels['ActivistsP'] = 'Activists'
node_labels['SkepticsP'] = 'Skeptics'
node_labels['OthersP'] = 'Others'
node_labels['Activists2P'] = 'Activists'
node_labels['Skeptics2P'] = 'Skeptics'
node_labels['Others2P'] = 'Others'
nx.draw_networkx_labels(G, pos, node_labels, font_size=12)

plt.suptitle(TITLE + '\nMODE: ' + MODE)
plt.axis('off')
plt.show()
