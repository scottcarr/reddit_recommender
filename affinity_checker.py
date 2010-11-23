#!/usr/bin/env python

import csv
import numpy
import matplotlib.pyplot as plt
import array

total_above = 0
total_below = 0

f = open("publicvotes-20101018_affinities.dump")

affs = array.array('f')

reader = csv.reader(f, delimiter="\t")
for row in reader:
	if float(row[2]) >= .5:
		total_above += 1
	else:
		total_below += 1
	affs.append(float(row[2]))

a = numpy.array(affs)

plt.hist(a)
plt.xlabel('Affinity')
plt.ylabel('Count')
plt.show()
print "Total above:", total_above
print "Total below:", total_below
print "Percent good:", total_above*100.00/(total_above+total_below)

f.close()
