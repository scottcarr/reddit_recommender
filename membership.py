def build_membership(usr_filename,clust_filename):
	"""
        outputs a list the contains the cluster_id for every
	user. It is of the form:
	memberships['user_id'] = cluster_to_which_that_UID_belongs
        """	
	f_usr = open(usr_filename,'r')
	f_clust = open(clust_filename,'r')
	memberships = {}
	i = 0
	usr = f_usr.readlines()
	for line in f_clust:
		memberships[usr[i][:-1]] = line[:-1]
		i+=1
	f_usr.close()
	f_clust.close()
	return memberships
