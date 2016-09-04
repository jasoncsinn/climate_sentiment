### This is setting the predictor

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

refresh1 = open('april_tweets_day.txt','w')
refresh1.close()
refresh2 = open('may_tweets_day.txt','w')
refresh2.close()
refresh3 = open('june_tweets_day.txt','w')
refresh3.close()
refresh4 = open('july_tweets_day.txt','w')
refresh4.close()
refresh5 = open('august_tweets_day.txt','w')
refresh5.close()
refresh6 = open('september_tweets_day.txt','w')
refresh6.close()
refresh7 = open('october_tweets_day.txt','w')
refresh7.close()
refresh8 = open('day_counts.py','w')
refresh8.close()


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
        sent = gscv.predict(test)[0]
        #print(sent)
        
        
        tweets_file2 = open(month + '_tweets_day.txt','a')
        tweets_file2.write(day + ' ::---:: ' + sent + '\n')
        tweets_file2.close()
    
    tweets_file3 = open(month + '_tweets_day.txt','r')
    activist = {}
    skeptical = {}
    neutral = {}
    for aline in tweets_file3:
        sentiment = aline.split(' ::---:: ')[1]
        num = aline.split(' ::---:: ')[0]
        if sentiment == 'activist\n':
            if num not in activist:
                activist[num] = 0
            activist[num] += 1
        if sentiment == 'skeptical\n':
            if num not in skeptical:
                skeptical[num] = 0
            skeptical[num] += 1
        if sentiment == 'neutral\n':
            if num not in neutral:
                neutral[num] = 0
            neutral[num] += 1        
    tweets_file3.close()
    
    x = np.array([])
    y = np.array([])
    for i in activist:
        x = np.append(x,[int(i)])
        y = np.append(y,[activist[i]])
        
    m = np.array([])
    n = np.array([])
    for j in skeptical:
        m = np.append(m,[int(j)])
        n = np.append(n,[skeptical[j]])
        
    u = np.array([])
    v = np.array([])
    for k in neutral:
        u = np.append(u,[int(k)])
        v = np.append(v,[neutral[k]])    
    
    save_file = open('day_counts.py','a')
    save_file.write(month + ':\nactivists:\n' + str(x) + '\n' + str(y) + '\nskeptical:\n' + str(m) + '\n' + str(n) + '\nneutrals:\n' + str(u) + '\n' + str(v))
    save_file.close()
        
        
    print(x)
    print(y)
    print(m)
    print(n)
    print(u)
    print(v)
    
    '''
    plt.scatter(x,y, color = 'red')
    plt.scatter(m,n)
    plt.scatter(u,v, color = 'black')
    #plt.axis([5,15, 0, 30])
    plt.show()
    print('did it work?')'''
        
            
    
        
        
###

prep('april')
prep('may')
prep('june')
prep('july')
prep('august')
prep('september')
prep('october')









### This is mapping it


'''import matplotlib.pyplot as plt
import numpy as np

N = 10
x = np.array([1,2,3,4,5])
y = np.array([1,2,3,4,5])
m = np.array([5,4,3,2,1])
n = np.array([1,2,3,4,5])

plt.scatter(x,y)
plt.scatter(m,n)
plt.show()'''