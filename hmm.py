import numpy as np
import pdb

from hmmlearn import hmm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2

states = ['A', 'S', 'O']
n_states = len(states)

observations = ['A', 'S', 'O']
n_observations = len(observations)

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

X_sent = []
texts = []
sents = []

with open('data/bernie_tweet_data.txt') as f:
	for line in f:
		text, _, _, _, sent = line.split(' ::---:: ', 4)
		sent = sent.strip('\n')
		X_sent.append([encoder[sent]])
		sents.append(encoder[sent])
		texts.append(text)	

pdb.set_trace()

model = hmm.MultinomialHMM(n_components=3, params='t', init_params='t')
model.startprob_ = start_prob
model.emissionprob_ = emission_probs
model = model.fit(X_sent)
np.set_printoptions(suppress=True)
print("Start distribution: ")
print(model.startprob_)
print("Transition matrix: ")
print(model.transmat_)
print('Emission matrix: ')
print(model.emissionprob_)

prediction = model.predict(X_sent)
print('HMM prediction: ' + ' '.join([states[p] for p in prediction]))
print('2stepsvm prediction: ' + ' '.join([states[s] for s in sents]))

with open('data/bernie_hmm_data.txt', 'w') as f:
	for i in range(len(sents)):
		to_write = states[prediction[i]] + " ::---:: "
		to_write += states[sents[i]] + " ::---:: "
		to_write += texts[i] + "\n"
		f.write(to_write)

num_correct = sum([1 for i,j in zip(prediction,sents) if i == j])
acc = 100.0 * num_correct / len(X_sent)

print("Number of correct states predicted: " + str(num_correct))
print("Accuracy: " + str(acc))
