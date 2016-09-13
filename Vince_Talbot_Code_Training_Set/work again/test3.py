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

testfile = open('tweets_sentiment.txt','r')

i = 0

for line in testfile:
    sentiment = line.split(' ::---:: ')[0]
    if sentiment == 'redundant':
        continue
    tweet = line.split(' ::---:: ')[1]
    
    tweets_file = open('tweets_sentiment2.txt','w')
    tweets_file.write(tweet)
    tweets_file.close()
    
    test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
    results = gscv.predict(test)
    
    if sentiment != results[0] and sentiment == 'activist':
        print('guess: ' + results[0] + '\nactual: ' + sentiment + '\ntweet: ' + tweet + '\n\n')
        i += 1
print(i)