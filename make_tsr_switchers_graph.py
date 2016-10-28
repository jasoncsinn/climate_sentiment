import datetime
import matplotlib.pyplot as plt
import numpy as np

import pdb
import sys

# Logger
class Logger(object):
	def __init__(self):
		self.terminal = sys.stdout
		self.log = open("data/tsr_cop21/results.txt", "a")
	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
	def flush(self):
		pass
sys.stdout = Logger()

s = [0, 0, 0, 0, 0, 0] # [to_a[0], to_n[0], to_a[last], to_n[last], numorig, numfinal]
a = [0, 0, 0, 0, 0, 0]
n = [0, 0, 0, 0, 0, 0]

MODE = "LAST"

with open('data/tsr_cop21/switcher_cop21.txt') as f:
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
