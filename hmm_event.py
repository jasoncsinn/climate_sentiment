import numpy as np
import pdb

from hmmlearn import hmm

states = ['A', 'S', 'O']

encoder = {}
encoder['a'] = 0
encoder['s'] = 1
encoder['n'] = 2

start_prob = np.array([0.33, 0.33, 0.34])

emission_probs = np.array([
	[0.64, 0.03, 0.33],
	[0.23, 0.26, 0.51],
	[0.21, 0.04, 0.75]
])

sentiments = []
lens = []

with open('data/tsr_trump/switcher_trump.txt') as f:
	for line in f:
		_, _, _, sents = line.split(' ', 3)
		sent_list = sents.strip('\n').split(' ')
		# convert to hmmlearn format.
		sent_list = [[encoder[i]] for i in sent_list]
		lens.append(len(sent_list))
		sentiments.append(sent_list)

X_sents = np.concatenate(sentiments, axis=0)

pdb.set_trace()

model = hmm.MultinomialHMM(n_components=3, params='t', init_params='t')
model.startprob_ = start_prob
model.emissionprob_ = emission_probs
model = model.fit(X_sents,lengths=lens)
np.set_printoptions(suppress=True)
print("Start distribution: ")
print(model.startprob_)
print("Transition matrix: ")
print(model.transmat_)
print("Emission matrix: ")
print(model.emissionprob_)

prediction = model.predict(X_sents)

with open('data/tsr_trump/hmm_data.txt', 'w') as f:
	to_write = "Start distribution: \n" + str(model.startprob_) + "\n"
	to_write += "Transition matrix: \n" + str(model.transmat_) + "\n"
	to_write += "Emission matrix: \n" + str(model.emissionprob_) + "\n"
	for i in range(len(X_sents)):
		to_write += "clf: " + states[X_sents[i][0]]
		to_write += " hmm: " + states[prediction[i]] + "\n"
	f.write(to_write)
