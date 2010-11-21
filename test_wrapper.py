#!/usr/bin/env python	

import random
import os

PERCENT_TEST = .20

#need to chop up affinities.dump

length = 0
#we want to know how big the file is
with open("publicvotes-20101018_affinities.dump") as f:
	for line in f:
		length += 1 

test_set_size = int(length*PERCENT_TEST)
test_set_idexes = random.sample(range(length), test_set_size)
test_set_dict = {}
for index in test_set_idexes:
	test_set_dict[index] = 1

training_set = []
test_set = []
i = 0
with open("publicvotes-20101018_affinities.dump") as f:
	for line in f:
		if i in test_set_dict:
			test_set.append(line)		
		else:
			training_set.append(line)
		i += 1

with open("test_dataset",'w') as f:
	for line in test_set:
		f.write(line)

with open("training_dataset",'w') as f:
	for line in training_set:
		f.write(line)

os.system("cat training_dataset | ./srrecs.py \"write_matrix('affinities.cm', 'affinities.clabel', 'affinities.rlabel')\"")

os.system("R -f ./srrecs.r")
