check_file = open('tweets_sentiment_refined.txt','r')
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

check_file.close()

check_file = open('tweets_sentiment_refined.txt','r')
i = a = 0
for line in check_file:
    i += 1
    if line.split(' ::---:: ')[0] == 'neutral':
        a += 1
print('\n' + str(i))
print( str(a) + ' actual neutrals')
check_file.close()