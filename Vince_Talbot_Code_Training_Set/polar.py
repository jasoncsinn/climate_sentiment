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


day = open('aug_15_2015.txt','r')
for line in day:
    tweet = line.split('":::text: "')[1].split('":::id: ')[0]
    user = line.split('')[1].split('')[0]
    
    tweets_file = open('tweets_sentiment2.txt','w')
    tweets_file.write(tweet)
    tweets_file.close()
    
    test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
    results = gscv.predict(test)
    
    s = a = n = 0
    lou = {}
    
    if results == 'activist':
        a += 1
        if a < 50:
            lou[user] = []
    if results == 'skeptical':
        s +=1
        if s < 50:
            lou[user] = []
    if results == 'neutral':
        n += 1
        if n < 50:
            lou[user] = []
    if a >= 50 and s>= 50 and n>= 50:
        break
day.close()

file = open('climate.txt','r')
for line in file:
    idnum = line.split('')[1].split('')[0]
    if idnum in lou:
        tweet = line.split('":::text: "')[1].split('":::id: ')[0]
        tweets_file = open('tweets_sentiment2.txt','w')
        tweets_file.write(tweet)
        tweets_file.close()
        
        test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
        results = gscv.predict(test)   
        
        lou[idnum] += [results]
        
file.close()

last = open('store.py','w')
last.write(str(lou))
last.close()
    