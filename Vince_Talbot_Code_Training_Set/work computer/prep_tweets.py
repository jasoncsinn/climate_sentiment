from random import shuffle

climate_file = open('tweets_sentiment_refined.txt','r')
alist = []
nlist = []
slist = []
a = s = n = 0

for line in climate_file:
        sentiment = line.split(' ::---:: ')[0]
        if sentiment == 'redundant':
                continue
        tweet = line.split(' ::---:: ')[1]
        if sentiment == 'activist':
                alist += [[tweet, 'activist']]
                a += 1
        if sentiment == 'neutral':
                nlist += [[tweet, 'neutral']]
                n += 1
        if sentiment == 'skeptical':
                slist += [[tweet, 'skeptical']]
                s += 1



#######
train = alist + nlist + slist
#######

train_tweets = open('train_tweets.txt','w')
train_sent = open('train_sentiments.txt','w')

for i in train:
        train_tweets.write(i[0])
        train_sent.write(i[1] + '\n')

train_tweets.close()
train_sent.close()
climate_file.close()

print('a = ' + str(a) + '\nn = ' + str(n) + '\ns = ' + str(s))