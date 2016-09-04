train_sent = open('train_sentiments.txt','r')

Y = []
for line in train_sent:
    Y += [line[0:-1]]

train_sent.close()

import numpy
import codecs
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer

word_vectorizer = CountVectorizer(analyzer='word')
X = word_vectorizer.fit_transform(codecs.open('train_tweets.txt','r','utf8'))

clf = LinearSVC()

params_space = { 'C': numpy.logspace(-6,0,11), 'class_weight':[None,'auto']}
gscv = GridSearchCV(clf,params_space,cv=3)

gscv.fit(X, Y)


#####
#####

s = 0
a = 0
lou = {}

day = open('polar_dates.txt','r')
for line in day:
    tweet = line.split('":::text: "')[1].split('":::id: ')[0]
    user = line.split('":::id: ')[1].split(' :::screen name:')[0]
    
    tweets_file = open('tweets_sentiment2.txt','w')
    tweets_file.write(tweet)
    tweets_file.close()
    
    test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
    results = gscv.predict(test)[0]
    
    if results == 'activist':
        a += 1
        if a < 500:
            lou[user] = []
    if results == 'skeptical':
        s +=1
        if s < 500:
            lou[user] = []
    '''if results == 'neutral':
        n += 1
        if n < 10:
            lou[user] = []'''
    if a >= 1000 and s>= 1000:
        break
day.close()

print('got it')

file = open('all_dates.txt','r')
for line in file:
    idnum = line.split('":::id: ')[1].split(' :::screen name:')[0]
    if idnum in lou:
        tweet = line.split('":::text: "')[1].split('":::id: ')[0]
        tweets_file = open('tweets_sentiment2.txt','w')
        tweets_file.write(tweet)
        tweets_file.close()
        
        test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
        results = gscv.predict(test)[0]   
        
        lou[idnum] += [results]
        
file.close()

print(lou)
last = open('store.py','w')
last.write(str(lou))
last.close()
    