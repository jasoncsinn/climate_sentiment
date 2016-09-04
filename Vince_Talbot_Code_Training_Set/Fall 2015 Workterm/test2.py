check_file = open('tweets_sentiment.txt','r')
s = n = a = r = i = 0
for line in check_file:
    i += 1
    sent = line.split(' ::---:: ')[0]
    if sent == 'skeptical':
        s += 1
    if sent == 'neutral':
        n += 1
    if sent == 'activist':
        a += 1
    if sent == 'redundant':
        r += 1
print('\n' + str(s) + ' skeptics \n' + str(n) + ' neutrals \n' + str(a) + ' activists \n' + str(r) + ' redundants \n \n' + str(s+a+n)+ ' useful \n \n' + str(s+n+a+r) + ' total \n' + str(i) + ' total lines')