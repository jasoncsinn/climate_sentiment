import matplotlib.pyplot as plt
import pdb
import numpy as np
import sys

event = 'trump'
print('Event: ' + event + '\n----------\n')

class Logger(object):
	def __init__(self):
		self.terminal = sys.stdout
		self.log = open('analysis/entropy_distributions/' + event + '.txt', 'a')
	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
	def flush(self):
		pass
sys.stdout = Logger()

pre_a_ents = []
post_a_ents = []
pre_a_ht = {}
post_a_ht = {}

pre_s_ents = []
post_s_ents = []
pre_s_ht = {}
post_s_ht = {}

pre_n_ents = []
post_n_ents = []
pre_n_ht = {}
post_n_ht = {}

with open('data/tsr_' + event + '/pre_data.txt') as f:
	for line in f:
		line = line.strip('\n').split(' ::---:: ')
		if len(line) == 6:
			_, _, _, _, sent, ent = line
			ent = float(ent) 
			bucket_ent = int(ent * 100)
			if sent == 'a':
				pre_a_ht[bucket_ent] = pre_a_ht.get(bucket_ent, 0) + 1
				pre_a_ents.append(ent)
			elif sent == 's':
				pre_s_ents.append(ent)
				pre_s_ht[bucket_ent] = pre_s_ht.get(bucket_ent, 0) + 1
			elif sent == 'n':
				pre_n_ents.append(ent)
				pre_n_ht[bucket_ent] = pre_n_ht.get(bucket_ent, 0) + 1

with open('data/tsr_' + event + '/post_data.txt') as f:
	for line in f:
		line = line.strip('\n').split(' ::---:: ')
		if len(line) == 6:
			_, _, _, _, sent, ent = line
			# Make buckets
			ent = float(ent)
			bucket_ent = int(ent * 100)
			if sent == 'a':
				post_a_ents.append(ent)
				post_a_ht[bucket_ent] = post_a_ht.get(bucket_ent, 0) + 1
			elif sent == 's':
				post_s_ents.append(ent)
				post_s_ht[bucket_ent] = post_s_ht.get(bucket_ent, 0) + 1
			elif sent == 'n':
				post_n_ents.append(ent)
				post_n_ht[bucket_ent] = post_n_ht.get(bucket_ent, 0) + 1

# Make mask
mask = range(max(pre_a_ht.keys()))
entropies = [i / 100.0 for i in mask]

# Make entropy counts
pre_a_values = [pre_a_ht.get(i,0) for i in mask]
post_a_values = [post_a_ht.get(i,0) for i in mask]

pre_a_values = [i * 100.0 / sum(pre_a_values) for i in pre_a_values]
post_a_values = [i * 100.0 / sum(post_a_values) for i in post_a_values]

pre_s_values = [pre_s_ht.get(i,0) for i in mask]
post_s_values = [post_s_ht.get(i,0) for i in mask]

pre_s_values = [i * 100.0 / sum(pre_s_values) for i in pre_s_values]
post_s_values = [i * 100.0 / sum(post_s_values) for i in post_s_values]

pre_n_values = [pre_n_ht.get(i,0) for i in mask]
post_n_values = [post_n_ht.get(i,0) for i in mask]

pre_n_values = [i * 100.0 / sum(pre_n_values) for i in pre_n_values]
post_n_values = [i * 100.0 / sum(post_n_values) for i in post_n_values]

# Find means
pre_a_mean = sum(pre_a_ents) / len(pre_a_ents)
post_a_mean = sum(post_a_ents) / len(post_a_ents)

pre_s_mean = sum(pre_s_ents) / len(pre_s_ents)
post_s_mean = sum(post_s_ents) / len(post_s_ents)

pre_n_mean = sum(pre_n_ents) / len(pre_n_ents)
post_n_mean = sum(post_n_ents) / len(post_n_ents)

# Find stds
pre_a_std = [np.power((x - pre_a_mean), 2) for x in pre_a_ents]
pre_a_std = np.power(sum(pre_a_std) / len(pre_a_std), 0.5)

post_a_std = [np.power((x - post_a_mean), 2) for x in post_a_ents]
post_a_std = np.power(sum(post_a_std) / len(post_a_std), 0.5)

pre_s_std = [np.power((x - pre_s_mean), 2) for x in pre_s_ents]
pre_s_std = np.power(sum(pre_s_std) / len(pre_s_std), 0.5)

post_s_std = [np.power((x - post_s_mean), 2) for x in post_s_ents]
post_s_std = np.power(sum(post_s_std) / len(post_s_std), 0.5)

pre_n_std = [np.power((x - pre_n_mean), 2) for x in pre_n_ents]
pre_n_std = np.power(sum(pre_n_std) / len(pre_n_std), 0.5)

post_n_std = [np.power((x - post_n_mean), 2) for x in post_n_ents]
post_n_std = np.power(sum(post_n_std) / len(post_n_std), 0.5)

ax1 = plt.subplot2grid((9,1),(0,0), rowspan=3)
ax1.plot(entropies, pre_a_values, '-', color='gray')
ax1.plot(entropies, post_a_values, '-', color='black')
ax1.axvline(x=pre_a_mean, linestyle='--', color='red')
ax1.axvline(x=post_a_mean, linestyle='-', color='red')

ax2 = plt.subplot2grid((9,1),(3,0), rowspan=3)
ax2.plot(entropies, pre_s_values, '-', color='gray')
ax2.plot(entropies, post_s_values, '-', color='black')
ax2.axvline(x=pre_s_mean, linestyle='--', color='red')
ax2.axvline(x=post_s_mean, linestyle='-', color='red')

if event == 'trump':
	ax31 = plt.subplot2grid((9,1),(6,0))
	ax32 = plt.subplot2grid((9,1),(7,0), rowspan=2)
	pre_ent_line = ax31.plot(entropies, pre_n_values, '-', color='gray')
	post_ent_line = ax31.plot(entropies, post_n_values, '-', color='black')
	pre_mean_line = ax31.axvline(x=pre_n_mean, linestyle='--', color='red')
	post_mean_line = ax31.axvline(x=post_n_mean, linestyle='-', color='red')
	pre_ent_line = ax32.plot(entropies, pre_n_values, '-', color='gray')
	post_ent_line = ax32.plot(entropies, post_n_values, '-', color='black')
	pre_mean_line = ax32.axvline(x=pre_n_mean, linestyle='--', color='red')
	post_mean_line = ax32.axvline(x=post_n_mean, linestyle='-', color='red')
else:
	ax3 = plt.subplot2grid((9,1),(6,0), rowspan=3)
	pre_ent_line = ax3.plot(entropies, pre_n_values, '-', color='gray')
	post_ent_line = ax3.plot(entropies, post_n_values, '-', color='black')
	pre_mean_line = ax3.axvline(x=pre_n_mean, linestyle='--', color='red')
	post_mean_line = ax3.axvline(x=post_n_mean, linestyle='-', color='red')

print('Activist distribution\n----------')
print ('Pre Mean: ' + str(pre_a_mean) + ' Pre std: ' + str(pre_a_std))
print ('Post Mean: ' + str(post_a_mean) + ' Post std: ' + str(post_a_std))
print('----------\n')

print('Denier distribution\n----------')
print('Pre Mean: ' + str(pre_s_mean) + ' Pre std: ' + str(pre_s_std))
print('Post Mean: ' + str(post_s_mean) + ' Post std: ' + str(post_s_std))
print('----------\n')

print('Neutral distribution\n----------')
print('Pre Mean: ' + str(pre_n_mean) + ' Pre std: ' + str(pre_n_std))
print('Post Mean: ' + str(post_n_mean) + ' Post std: ' + str(post_n_std))
print('----------\n')

ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)
ax1.axis([0,0.8,0,30])
ax2.axis([0,0.8,0,30])

if event == 'trump':
	ax32.set_autoscale_on(False)
	ax31.set_autoscale_on(False)
	ax31.axis([0,0.8,40,50])
	ax32.axis([0,0.8,0,20])
else:
	ax3.set_autoscale_on(False)
	ax3.axis([0,0.8,0,30])

ax1.tick_params(axis='x', labelbottom='off')
ax2.tick_params(axis='x', labelbottom='off')
if event == 'trump':
	ax31.tick_params(axis='x', which='both', bottom='off', labelbottom='off')
	ax32.tick_params(axis='x', which='both', top='off')
	ax31.spines['bottom'].set_visible(False)
	ax32.spines['top'].set_visible(False)

ax1.set_ylabel('Percent of Activists')
ax2.set_ylabel('Percent of Deniers')
if event == 'trump':
	ax32.set_xlabel('Entropy')
	ax32.text(-0.065, 31, 'Percent of Neutrals', rotation='vertical')
	ticks = range(40,51,5)
	ax31.set_yticks(ticks)
	ax31.set_yticklabels(ticks)
	ticks = range(0,21,5)
	ax32.set_yticks(ticks)
	ax32.set_yticklabels(ticks)
else:
	ax3.set_ylabel('Percent of Neutrals')
	ax3.set_xlabel('Entropy')

if event == 'trump':
	d = .008  # how big to make the diagonal lines in axes coordinates
	kwargs = dict(transform=ax31.transAxes, color='k', clip_on=False)
	ax31.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
	ax31.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

	kwargs.update(transform=ax32.transAxes)  # switch to the bottom axes
	ax32.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
	ax32.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

#plt.tight_layout()
ax1.legend((pre_ent_line[0],post_ent_line[0], pre_mean_line, post_mean_line), ('Before Distribution', 'After Distribution', 'Before Mean', 'After Mean'), prop={'size':10}, loc=2)

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
plt.savefig('analysis/entropy_distributions/' + event + '.eps', format='eps')
plt.show()
