train_sent = open('train_sentiments.txt','r')
test_sent = open('test_sentiments.txt','r')

Y = []
for line in train_sent:
    Y += [line[0:-1]]
    
Z = []
for line in test_sent:
    Z += [line[0:-1]]

train_sent.close()
test_sent.close()



import numpy
import codecs
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer

word_vectorizer = CountVectorizer(analyzer='word')
X = word_vectorizer.fit_transform(codecs.open('train_tweets.txt','r','utf8'))

clf = LinearSVC()

params_space = { 'C': numpy.logspace(-5,0,10), 'class_weight':[None,'auto']}
gscv = GridSearchCV(clf,params_space,cv=2)

gscv.fit(X, Y)

testset = word_vectorizer.transform(codecs.open('test_tweets.txt','r','utf8'))
results = gscv.predict(testset)
#print(results[0::])

correct = wrong = total = 0
wl = []

for i in results:
    total += 1
    if i == Z[total - 1]:
        correct += 1
    else:
        wrong += 1
        wl += [Z[total - 1]]

percent_right = correct/total * 100    
print(str(correct) + ' correct \n' + str(wrong) + ' wrong \n' + str(total) + ' total \n' + str(percent_right) + '% correct')

s = a = n = 0

for i in wl:
    if i == 'skeptical':
        s += 1
    if i == 'neutral':
        n += 1
    if i == 'activist':
        a += 1

print('\nWrong breakdown:\n' + str(s) + ' skeptical\n' + str(n) + ' neutral\n' + str(a) + ' activist')