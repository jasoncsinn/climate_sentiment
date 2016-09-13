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

params_space = { 'C': numpy.logspace(-6,0,11), 'class_weight':[None,'auto']}
gscv = GridSearchCV(clf,params_space,cv=3)

gscv.fit(X, Y)
print(gscv.best_estimator_, gscv.best_params_, gscv.best_score_)

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








'''
######## helper function ##########
## determines if the tweet has already been processed
## will return true if it has been
def already_in(twt):
        a = False
        check_file = open('tweets_sentiment3.txt','r')
        for aline in check_file:
            if twt in aline:
                if 'redundant' in aline:
                    break
                else:
                    a = True
                    break
        check_file.close()
        return a




###### main program #########
climate_file = open('climate_19_Jul_2015.txt','r')
#climate_file = codecs.open('climate_19_Jul_2015.txt','r','utf8')

for line in climate_file:
        sentiment = ''
        tweet = line.split('":::text: "')[1].split('":::id: ')[0]
        if already_in(tweet):
                print('Already have that tweet')
                continue
        
        print('\n' + tweet + '\n')
        ans = input('1:skeptical, 2:neutral, 3:activist, 4:redundant --- type "end" to quit \n')
        while (ans != 'end') and (ans != '1') and (ans != '2') and (ans != '3') and (ans != '4'):
                ans = input('1:skeptical, 2:neutral, 3:activist, 4;redundant --- type "end" to quit \n')
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
        tweets_file = open('tweets_sentiment2.txt','w')
        tweets_file.write(tweet)
        tweets_file.close()
        
        tweets_file3 = open('tweets_sentiment3.txt','a')
        tweets_file3.write(sentiment + ' ::---:: ' + tweet + '\n')
        tweets_file3.close()        
        
        test = word_vectorizer.transform(codecs.open('tweets_sentiment2.txt','r','utf8'))
        results = gscv.predict(test)
        print('\n' + results[0] + '\n')
        
        
        
        rw_file = open('right_wrong.txt','a') 
                
        if results[0] == sentiment:
            print('correct')
            rw_file.write('correct\n')
        else:
            print('wrong \n guess: ' + results[0] + '\n actual: ' + sentiment)
            rw_file.write('wrong\n')
            
            answer = input('Would you like to add this tweet to the training set? (y or n)\n')
            while answer != 'y' and answer != 'n':
                answer = input('Would you like to add this tweet to the training set? (y or n)\n') 
            
            if answer == 'y':
                add = open('tweets_sentiment_refined.txt','a')
                add.write(sentiment + ' ::---:: ' + tweet)
                add.close()
            
        rw_file.close()
        
rw_file2 = open('right_wrong.txt','r')
r = w = 0

for line in rw_file2:
    if 'correct' in line:
        r += 1
    if 'wrong' in line:
        w += 1
print(r)
print(w)
per = (r / (r + w)) * 100       
print(str(r) + ' right\n' + str(w) + ' wrong\n' + str(per) + ' % correct')        

rw_file2.close()
climate_file.close()
'''