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

params_space = { 'C': numpy.logspace(-5,0,10), 'class_weight':[None,'auto']}
gscv = GridSearchCV(clf,params_space,cv=2)

gscv.fit(X, Y)

"""testset = word_vectorizer.transform(codecs.open('test_tweets.txt','r','utf8'))
results = gscv.predict(testset)
#print(results[0::])"""



###### main program #########
#climate_file = codecs.open('climate_19_Jul_2015.txt','r','utf8')       
        
        test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
        results = gscv.predict(test)
        print('\n' + results[0] + '\n')
        
