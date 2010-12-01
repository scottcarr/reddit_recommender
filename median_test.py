#!/usr/bin/env python
import cluster_aff
import numpy
import matplotlib.pyplot as plt
import pdb

medians = cluster_aff.generate_median_sr_affs('training_dataset')
a = numpy.array(medians.values())
pdb.set_trace()
plt.hist(a)
plt.xlabel('Affinity')
plt.ylabel('Count')
plt.show()
