'''### This is setting the predictor

train_sent = open('train_sentiments.txt','r')

Y = []
for line in train_sent:
    Y += [line[0:-1]]

train_sent.close()

import numpy as np
import codecs
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer

word_vectorizer = CountVectorizer(analyzer='word')
X = word_vectorizer.fit_transform(codecs.open('train_tweets.txt','r','utf8'))

clf = LinearSVC()

params_space = { 'C': np.logspace(-5,0,10), 'class_weight':[None,'auto']}
gscv = GridSearchCV(clf,params_space,cv=2)

gscv.fit(X, Y)

#results = gscv.predict(testset)
#print(results[0::])

### This is applying the predictor

import matplotlib.pyplot as plt

### Helper function:
### will take in the month of tweets and return

def prep(month):
    afile = open(month + '_tweets.txt','r')
    for line in afile:
        split = line.split(' ::---:: ')
        tweet = split[1]
        day = split[0][-2::]
        
        tweets_file = open('tweet_temp.txt','w')
        tweets_file.write(tweet)
        tweets_file.close()
        
        test = word_vectorizer.transform(codecs.open('tweet_temp.txt','r','utf8'))
        sent = gscv.predict(test)        
        
        tweets_file2 = open(month + '_tweets_day.txt','a')
        tweets_file2.write(day + ' ::---:: ' + sent + '\n')
        tweets_file2.close()
    
    tweets_file3 = open(month + '_tweets_day.txt','r')
    activist = {}
    skeptical = {}
    for aline in tweets_file3:
        sentiment = aline.split(' ::---:: ')[1]
        num = aline.split(' ::---:: ')[0]
        if sentiment == 'activist':
            if num not in activist:
                activist[num] = 0
            activist[num] += 1
        if sentiment == 'skeptical':
            if num not in skeptical:
                skeptical[num] == 0
            skeptical[num] += 1
    tweets_file3.close()
    
    x = np.array([])
    y = np.array([])
    for i in activist:
        x = np.append(x,[int(i)])
        y = np.append(x,[activist[i]])
    
    plt.scatter(x,y)
    plt.show() 
        
            
    
        
        
###

prep('apr')
#prep('may')
#prep('jun')
#prep('jul')
#prep('aug')
#prep('sep')









### This is mapping it
'''

import matplotlib.pyplot as plt
import numpy as np

N = 10
x = np.array([1,2,3,4,5])
y = np.array([1,2,3,4,5])
m = np.array([5,4,3,2,1])
n = np.array([1,2,3,4,5])

plt.scatter(x,y)
plt.scatter(m,n)
plt.show()