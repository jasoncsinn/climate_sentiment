######## helper function ##########
## determines if the tweet has already been processed
## will return true if it has been
def already_in(twt):
        a = False
        check_file = open('tweets_sentiment.txt','r')
        for aline in check_file:
                if twt in aline:
                        a = True
                        break
        check_file.close()
        return a




###### main program #########
climate_file = open('climate_4_Sep_2015.txt','r')

for line in climate_file:
        sentiment = ''
        tweet = line.split('":::text: "')[1].split('":::id: ')[0]
        if already_in(tweet):
                print('Already have that tweet')
                continue
        
        print('\n' + tweet + '\n')
        ans = input('1:skeptical, 2:neutral, 3:activist, 4:redundant --- type "end" to quit \n')
        while (ans != 'end') and (ans != '1') and (ans != '2') and (ans != '3') and (ans != '4'):
                ans = input('1:skeptical, 2:neutral, 3:activist, type "end" to quit \n')
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
        tweets_file = open('tweets_sentiment.txt','a')
        tweets_file.write(sentiment + ' ::---:: ' + tweet +'\n')
        tweets_file.close()
        
climate_file.close()