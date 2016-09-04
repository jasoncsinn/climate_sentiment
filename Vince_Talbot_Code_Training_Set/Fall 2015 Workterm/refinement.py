check = 'activist'
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
old_file = open('tweets_sentiment.txt','r')

for line in old_file:
        sentiment = ''
        tweet = line.split(' ::---:: ')[1]
        if line.split(' ::---:: ')[0] != check or already_in(tweet):
                print('Already have that tweet')
                continue
        
        print('\n' + tweet)
        ans = input(check + ' --- 1:skeptical, 2:neutral, 3:activist, 4:redundant --- type "end" to quit \n')
        while (ans != 'end') and (ans != '1') and (ans != '2') and (ans != '3') and (ans != '4'):
                ans = input(check + ' --- 1:skeptical, 2:neutral, 3:activist, 4;redundant --- type "end" to quit \n')
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
        new_file = open('tweets_sentiment_refined.txt','a')
        new_file.write(sentiment + ' ::---:: ' + tweet)
        new_file.close()
        
old_file.close()