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


######## helper function ##########
## determines if the tweet has already been processed
## will return true if it has been
def already_in(twt):
        a = False
        check_file = open('tweets_sentiment_refined.txt','r')
        for aline in check_file:
                if twt in aline:
                        a = True
                        break
        check_file.close()
        return a




###### main program #########
climate_file = open('neut.txt','r')

for line in climate_file:
        sentiment = ''
        tweet = line.split('":::text: "')[1].split('":::id: ')[0]
        if already_in(tweet):
                print('Already have that tweet')
                continue
        
        print('\n' + tweet + '\n')
        ans = input('1:skeptical, 2:neutral, 3:activist, 4:redundant, 5:test --- type "end" to quit \n')
        while (ans != 'end') and (ans != '1') and (ans != '2') and (ans != '3') and (ans != '4') and (ans != '5'):
                ans = input('1:skeptical, 2:neutral, 3:activist, 4:redundant, 5:test --- type "end" to quit \n')
        if ans == '5':
            tweets_file = open('tweets_sentiment2.txt','w')
            tweets_file.write(tweet)
            tweets_file.close()
            
            test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
            results = gscv.predict(test)
            print('\n' + results[0] + '\n')
            ans = input('1:skeptical, 2:neutral, 3:activist, 4:redundant --- type "end" to quit \n')    
        
        if ans == 'end':
                break
        if ans == '1':
                sentiment = 'skeptical'
        if ans == '2':
                sentiment = 'neutral'
        if ans == '3':
                sentiment = 'activist'
        if ans == '4':
                sentiment = 'redundant'
        
                        
                
        tweets_file = open('tweets_sentiment_refined.txt','a')
        tweets_file.write(sentiment + ' ::---:: ' + tweet +'\n')
        tweets_file.close()
        
climate_file.close()