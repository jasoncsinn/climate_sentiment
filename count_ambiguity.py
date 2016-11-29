import sys

class Logger(object):
	def __init__(self):
		self.terminal = sys.stdout
		self.log = open('data/ambiguity.log', 'a')
	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
	def flush(self):
		pass
sys.stdout = Logger()

num_pre = [0,0,0,0]

NAME = 'earthday'
print('Generating pre and post distributions for event name: ' + NAME)

with open('data/tsr_' + NAME + '/pre_data.txt') as f:
	for line in f:
		_,_,_,_,sent = line.split(' ::---:: ', 4)
		sent = sent.strip('\n')
		if sent == 'a':
			num_pre[0] += 1
		if sent == 's':
			num_pre[1] += 1
		if sent == 'n':
			num_pre[2] += 1
		if sent == 'u':
			num_pre[3] += 1

pre_total = sum(num_pre)
normalized_pre = [n * 100.0 / pre_total for n in num_pre]
print('\nPrior to event\n----------')
print('Raw number of tweets: ' + str(num_pre))
print('Total number of tweets: ' + str(pre_total))
print('Normalized distribution: ' + str(normalized_pre))
print('----------\n')

num_post = [0,0,0,0]

with open('data/tsr_' + NAME + '/post_data.txt') as f:
	for line in f:
		_,_,_,_,sent = line.split(' ::---:: ', 4)
		sent = sent.strip('\n')
		if sent == 'a':
			num_post[0] += 1
		if sent == 's':
			num_post[1] += 1
		if sent == 'n':
			num_post[2] += 1
		if sent == 'u':
			num_post[3] += 1

post_total = sum(num_post)
normalized_post = [n * 100.0 / post_total for n in num_post]
print('After event\n----------')
print('Raw number of tweets: ' + str(num_post))
print('Total number of tweets: ' + str(post_total))
print('Normalized distribution: ' + str(normalized_post))
print('----------\n')
