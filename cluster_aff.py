import csv
import pdb
from operator import itemgetter
import heapq
import math

def sum_cluster_affinities(memberships, aff_filename):
	"""
        takes the user_id, cluster_id pairs from memberships
	and sums the affinities for every subreddit that a user
	of a given cluster has voted on
	output form: clusters['cluster_id']['subreddit_id'] = sumed_affinity
        """
	
	f_aff = open(aff_filename)

	aff_reader = csv.reader(f_aff,delimiter='\t')

	clusters = {}
	for row in aff_reader:
		#each for in aff file is a tuple, so need to get the parts
		user_id = row[0]
		sr_id = row[1]
		affinity = float(row[2])
		try:
			c_id = int(memberships[user_id])
			try:
				#this will only work if the cluster_ID,sr_id exists
				clusters[c_id][sr_id] += affinity
			except KeyError:
				#either that cluster id or the sr_id didn't exist,
				#so we must initialize it
				try:
					clusters[c_id][sr_id] = affinity
				except KeyError:
					#must be the first time for  the cluster_id		
					clusters[c_id] = { sr_id : affinity } 
		except KeyError:
			#apparently not all UIDs in clabel are in the output of srrecs.r	 
			#print user_id, "in affinities.clabel but not in srrecs.r output"
                        pass
	f_aff.close()
	return clusters

def check_recommendations(memberships, top_srs, test_data_file, threshold, medians):		
	""" 
        takes the top recommended subreddits (top_srs) and checks that
        the members of the associated cluster have affinities above a 
        threshold for the recommended subreddits
        """
        
        f_aff = open(test_data_file)
	aff_reader = csv.reader(f_aff,delimiter='\t')
	
	total_good = 0
	total_bad = 0		
        totals = [0,0]
	
        for row in aff_reader:
		#each for in aff file is a tuple, so need to get the parts
		user_id = row[0]
		sr_id = row[1]
		affinity = float(row[2])
		
                try:
                        cluster = int(memberships[user_id])
                        if sr_id in top_srs[cluster]:
                                #if affinity >= threshold:
                                #       total_good += 1
                                #else:
                                #        total_bad += 1
                                try:
					if affinity >= medians[sr_id]:
					       total_good += 1
					else:
						total_bad += 1
				except KeyError:
					print "That's weird, that subreddit wasn't found in the medians"
                except KeyError:
                        #not all UIDs in affinities.dump appear in affinities.clabel
                        pass

        totals[0] = total_good
        totals[1] = total_bad
        return totals

def generate_and_check_recommendations(memberships, test_data_file, threshold, clusters, n_top, test_data_size, medians): 
	""" 
        generates the top recommended subreddits (top_srs) and then calls 
        check_recommendations to check them.  Also outputs the total good and
        bad recommendations
        """
        good = 0
        bad = 0
        largest = range(0,len(clusters)+1)
        for i in range(1,len(clusters)+1):
                temp_largest = heapq.nlargest(n_top, clusters[i].iteritems(),itemgetter(1))
                largest[i] = {}
                for item in temp_largest:
                        largest[i][item[0]] =  item[1]

        totals = check_recommendations(memberships, largest, test_data_file,threshold, medians)
        good += totals[0]
        bad += totals[1]

        print "Total good recommendations:", good
        print "Total bad recommendations:", bad
	print "Total undefined:", test_data_size - good - bad
	print "Percent good:", float( good*100.00 / (bad + good) )
	print "Percent undefined:", (test_data_size - good - bad)*100.00/test_data_size 
	
	return [good , bad]

def generate_median_sr_affs(votes_file):
	f = open(votes_file,'r')
	reader = csv.reader(f, delimiter='\t')
	
	srs = {}

        for row in reader:
		#each for in aff file is a tuple, so need to get the parts
		user_id = row[0]
		sr_id = row[1]
		affinity = float(row[2])

		if not(sr_id in srs):
			srs[sr_id] = []
			srs[sr_id].append(affinity)
		else:
			srs[sr_id].append(affinity)
	medians = {}
	temp_list = []
	for sr_id  in srs:
		temp_list = sorted(srs[sr_id])
		middle_index = int(math.floor(len(temp_list)/2))
		if len(temp_list) % 2 == 0:
			#there is an even number of elements
			medians[sr_id] = (temp_list[middle_index]+temp_list[middle_index-1])/2
		else:
			#there is an odd number of elements		
			medians[sr_id] = temp_list[middle_index]
	return medians 
