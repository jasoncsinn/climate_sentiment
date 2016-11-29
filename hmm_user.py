import numpy as np
import pdb

from hmmlearn import hmm

hidden_states = ['A', 'S', 'O']
observable_states = ['A', 'S', 'O', 'U']

encoder = {}
encoder['a'] = 0
encoder['s'] = 1
encoder['n'] = 2
encoder['u'] = 3

start_prob = np.array([0.33, 0.33, 0.34])

#emission_probs = np.array([
#	[0.64, 0.03, 0.33],
#	[0.23, 0.26, 0.51],
#	[0.21, 0.04, 0.75]
#])

sents = []
sent_lens = []
lines = []

with open('data/hmm_data.txt') as f:
	for line in f:
		lines.append(line)
		_,user_sents = line.split(':')
		user_sents = user_sents.strip(' ').strip('\n')
		user_sents = user_sents.split(' ')
		for i in user_sents:
			sents.append(encoder[i])
		sent_lens.append(len(user_sents))

sents = np.array(sents).reshape(-1, 1)
pdb.set_trace()

model = hmm.MultinomialHMM(n_components=3, params='ets', init_params='et')
model.startprob_ = start_prob
#model.emissionprob_ = emission_probs
model = model.fit(sents, lengths=sent_lens)
np.set_printoptions(suppress=True)
print("Start distribution: ")
print(model.startprob_)
print("Transition matrix: ")
print(model.transmat_)
print('Emission matrix: ')
print(model.emissionprob_)


prediction = model.predict(sents, lengths=sent_lens)

with open('data/hmm_results.txt', 'w') as f:
	to_write = "Start distribution: \n" + str(model.startprob_) + "\n"
	to_write += "Transition matrix: \n" + str(model.transmat_) + "\n"
	to_write += "Emission matrix: \n" + str(model.emissionprob_) + "\n"
	for i in range(len(sents)):
		status = "hidden: " + hidden_states[prediction[i]]
		status += " observable: " + observable_states[sents[i]] + '\n'
		to_write += status

#		if hidden_states[prediction[i]] != observable_states[sents[i]] and observable_states[sents[i]] != 'O':
#			print(status)
	f.write(to_write)

