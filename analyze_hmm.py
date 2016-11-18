import pdb

with open('analysis/control_hmm_data.txt') as f:
	lines = f.readlines()
	lines = lines[10:]
	clf_score = 0
	hmm_score = 0
	for line in lines:
		line = line.split(' ', 6)
		if line[1] == line[3]:
			clf_score += 1
		if line[1] == line[5]:
			hmm_score += 1
	print("final clf score = " + str(clf_score) + "/" + str(len(lines)) + " = " + str(100.0*clf_score/len(lines)) + "%")
	print("final hmm score = " + str(hmm_score) + "/" + str(len(lines)) + " = " + str(100.0*hmm_score/len(lines)) + "%")
