#!/usr/bin/env python

import sys
import membership
import cluster_aff

def test_clusters(recommend_n_largest = 10, 
                  accuracy_threshold = 0.5, 
                  aff_clabel='affinities.clabel',
                  test_data_file = 'test_dataset',
		  training_data_file = 'training_dataset',
                  cluster_id_file = 'clusters_file',
                 ):
        """
        test clustering by building a list of the most popular 
        subreddits for a given reddit and then checking to see 
        if members of that cluster have an affinity 
        above a certain threshold for the recommended subreddits
        
        parameters:
                recommend_n_largest: 
                        how many of the strongest subreddits to recommend
                
                accuracy_threshold: 
                        if the user's affinity is above this, that 
                        is considered a "good" recommendation
                
                aff_clabel:
                        the file that contains the user_ids to
                        matchup with the output of skmeans
                
                aff_dump: 
                        the vote dump file
                
                cluster_id_file: 
                        file name of the output of skmeans (mat) 
        
        """

        # memberships is a dict, i.e. memberships['user_id'] = cluster_to which_the_user_belongs
        memberships = membership.build_membership(aff_clabel,cluster_id_file)

        # cluster is a dict where the keys are cluster ids (1...50) and the values are a list of users that
        # belong to that cluster
        clusters = cluster_aff.sum_cluster_affinities(memberships, training_data_file)

        #this does the actual testing and printing
        cluster_aff.generate_and_check_recommendations(memberships, test_data_file, accuracy_threshold, clusters, recommend_n_largest)

def iterate_n_largest(	min = 250,
		      	max = 300,
                  	accuracy_threshold = 0.5,
			aff_clabel='affinities.clabel',
                  	test_data_file = 'test_dataset',
		 	training_data_file = 'training_dataset',
                  	cluster_id_file = 'clusters_file',):

	test_data_size = 0
	with open(test_data_file) as f:
		for line in f:
			test_data_size += 1
	
	memberships = membership.build_membership(aff_clabel,cluster_id_file)

        clusters = cluster_aff.sum_cluster_affinities(memberships, training_data_file)

	for n in range(min,max):
		print "N =", n
		cluster_aff.generate_and_check_recommendations(	memberships, 
								test_data_file, 
								accuracy_threshold,
								clusters, 	
								n,
								test_data_size)	

if __name__ == '__main__':
        eval(sys.argv[1])
