import numpy
import codecs
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer

train_sent = open('train_sentiments.txt','r')
Y = []
for line in train_sent:
    Y += [line[0:-1]]
train_sent.close()


word_vectorizer = CountVectorizer(analyzer='word')
X = word_vectorizer.fit_transform(codecs.open('train_tweets.txt','r','utf8'))

clf = LinearSVC()

params_space = { 'C': numpy.logspace(-5,0,10), 'class_weight':[None,'auto']}
gscv = GridSearchCV(clf,params_space,cv=2)

gscv.fit(X, Y)

########

climate_file = open('climate_19_Jul_2015.txt','r')

i = 0

for line in climate_file:
        sentiment = ''
        tweet = line.split('":::text: "')[1].split('":::id: ')[0]
        
        tweets_file = open('tweets_sentiment2.txt','w')
        tweets_file.write(tweet)
        tweets_file.close()
        
        test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
        results = gscv.predict(test)        
        
        if results == 'neutral':
            sfile = open('neut.txt','a')
            sfile.write(line)
            sfile.close()
            i += 1
        
        if i > 100:
            break
            

        
climate_file.close()