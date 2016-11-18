import numpy as np
import pdb

from hmmlearn import hmm

hidden_states = ['A', 'S']
observable_states = ['A', 'S', 'O']

encoder = {}
encoder['a'] = 0
encoder['s'] = 1
encoder['n'] = 2

start_prob = np.array([0.5, 0.5])

emission_probs = np.array([
	[0.64, 0.03, 0.33],
	[0.23, 0.26, 0.51],
	[0.21, 0.04, 0.75]
])

X_sent = []
texts = []
sents = []

with open('data/hmm/control_tweet_data.txt') as f:
	for line in f:
		text, _, _, _, sent = line.split(' ::---:: ', 4)
		sent = sent.strip('\n')
		X_sent.append([encoder[sent]])
		sents.append(encoder[sent])
		texts.append(text)	

#pdb.set_trace()

model = hmm.MultinomialHMM(n_components=2, params='et', init_params='e')
model.startprob_ = start_prob
#model.emissionprob_ = emission_probs
model = model.fit(X_sent)
np.set_printoptions(suppress=True)
print("Start distribution: ")
print(model.startprob_)
print("Transition matrix: ")
print(model.transmat_)
print('Emission matrix: ')
print(model.emissionprob_)

prediction = model.predict(X_sent)

with open('data/hmm/control_hmm_data.txt', 'w') as f:
	to_write = "Start distribution: \n" + str(model.startprob_) + "\n"
	to_write += "Transition matrix: \n" + str(model.transmat_) + "\n"
	to_write += "Emission matrix: \n" + str(model.emissionprob_) + "\n"
	pdb.set_trace()
	for i in range(len(sents)):
		status = "hidden: " + hidden_states[prediction[i]]
		status += " observable: " + observable_states[sents[i]]
		status += " text: " + texts[i] + "\n"
		to_write += status

#		if hidden_states[prediction[i]] != observable_states[sents[i]] and observable_states[sents[i]] != 'O':
#			print(status)
	f.write(to_write)
