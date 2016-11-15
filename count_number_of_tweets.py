total = 0

with open('data/total_tweets_fixed.txt') as f:
	for line in f:
		date, num = line.split(' ')
		num = int(num.strip('\n'))
		total += num
print(total)
