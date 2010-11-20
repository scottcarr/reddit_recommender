#!/usr/bin/env python	

import sys
import random
import pdb

PERCENT_TEST = .20

#need to chop up affinities.dump

test = []
training = []

with open("publicvotes-20101018_affinities.dump") as f:
	for line in f:
		training.append(line)

test_set_size = int(len(training)*PERCENT_TEST)

print "Done reading file"

#pdb.set_trace()

for i in range(test_set_size):
	if i % 100 == 0:
		print i,"of,",test_set_size
	selected = random.choice(training)
	test.append(selected)
	training.remove(selected)

with open("test_dataset",'w') as f:
	for line in test:
		f.write(line)

with open("training_dataset",'w') as f:
	for line in training:
		f.write(line)

