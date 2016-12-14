import pdb

event = 'trump'

num_a_pre = 0
num_s_pre = 0
num_a_post = 0
num_s_post = 0

with open('data/tsr_' + event + '/pre_disc_data.txt') as f:
	for line in f:
		tokens = line.split(' ::---:: ')
		if len(tokens) == 5:
			tokens[4] = tokens[4].strip('\n')
			if tokens[4] == 'a':
				num_a_pre += 1
			if tokens[4] == 's':
				num_s_pre += 1
#		print(tokens[0])


with open('data/tsr_' + event + '/post_disc_data.txt') as f:
	for line in f:
		tokens = line.split(' ::---:: ')
		if len(tokens) == 5:
			tokens[4] = tokens[4].strip('\n')
			if tokens[4] == 'a':
				num_a_post += 1
			if tokens[4] == 's':
				num_s_post += 1
#	print(tokens[0])

print(str(num_a_pre) + " " + str(num_a_post))
print(str(num_s_pre) + " " + str(num_s_post))
