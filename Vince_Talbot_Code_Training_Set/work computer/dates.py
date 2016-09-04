all_tweets = open('all_dates.txt','r')

april = open('april_tweets.txt','w')
may = open('may_tweets.txt','w')
june = open('june_tweets.txt','w')
july = open('july_tweets.txt','w')
august = open('august_tweets.txt','w')
september = open('september_tweets.txt','w')
october = open('october_tweets.txt','w')

for line in all_tweets:
    month = line[19:22]
    day = line[23:25]
    tweet = line.split(':::text: "')[1].split('":::id: ')[0]
    if month == 'Apr':
        april.write('day: ' + day + ' ::---:: ' + tweet + '\n')
        continue
    if month == 'May':
        may.write('day: ' + day + ' ::---:: ' + tweet + '\n')
        continue
    if month == 'Jun':
        june.write('day: ' + day + ' ::---:: ' + tweet + '\n')
        continue
    if month == 'Jul':
        july.write('day: ' + day + ' ::---:: ' + tweet + '\n')
        continue
    if month == 'Aug':
        august.write('day: ' + day + ' ::---:: ' + tweet + '\n')
        continue
    if month == 'Sep':
        september.write('day: ' + day + ' ::---:: ' + tweet + '\n')
        continue
    if month == 'Oct':
        october.write('day: ' + day + ' ::---:: ' + tweet + '\n')
        continue    
    else:
        print(month)
        

all_tweets.close()
april.close()
may.close()
june.close()
july.close()
august.close()
september.close() 
october.close()