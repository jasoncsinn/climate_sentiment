from random import shuffle

climate_file = open('tweets_sentiment.txt','r')
alist = []
nlist = []
slist = []

for line in climate_file:
        sentiment = line.split(' ::---:: ')[0]
        if sentiment == 'redundant':
                continue
        tweet = line.split(' ::---:: ')[1]
        if sentiment == 'activist':
                alist += [[tweet, 'activist']]
        if sentiment == 'neutral':
                nlist += [[tweet, 'neutral']]
        if sentiment == 'skeptical':
                slist += [[tweet, 'skeptical']]

shuffle(alist)
shuffle(nlist)
shuffle(slist)

al = int(len(alist) * 0.7)
nl = int(len(nlist) * 0.7)
sl = int(len(slist) * 0.7)

train = alist[0:al] + nlist[0:nl] + slist[0:sl]
test = alist[al::] + nlist[nl::] + slist[sl::]

shuffle(train)
shuffle(test)

train_tweets = open('train_tweets.txt','w')
train_sent = open('train_sentiments.txt','w')
test_tweets = open('test_tweets.txt','w')
test_sent = open('test_sentiments.txt','w')

for i in train:
        train_tweets.write(i[0])
        train_sent.write(i[1] + '\n')
        
for j in test:
        test_tweets.write(j[0])
        test_sent.write(j[1] + '\n')


train_tweets.close()
train_sent.close()
test_tweets.close()
test_sent.close()
climate_file.close()