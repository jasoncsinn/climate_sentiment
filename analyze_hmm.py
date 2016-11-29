import pdb

with open('data/hmm_results.txt') as f:
	lines = f.readlines()
	lines = lines[10:]

	score = 0
	nums = [0, 0, 0]
	for line in lines:
		line = line.split(' ', 3)
		if line[1] == line[3].strip('\n'):
			score += 1
		if line[1] == 'A':
			nums[0] += 1
		if line[1] == 'S':
			nums[1] += 1
		if line[1] == 'O':
			nums[2] += 1
	print("final score = " + str(score) + "/" + str(len(lines)) + " = " + str(100.0*score/len(lines)) + "%")
	print(str(nums))
