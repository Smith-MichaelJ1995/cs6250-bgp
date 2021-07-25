def generate_results():
	# Replace the contents of this cell with your code for Task 1 part A
	results = {}
	notebook_path = os.path.abspath("main.py")
	rib_files_directory_path = os.path.join(os.path.dirname(notebook_path), "rib_files")
	rib_files = os.listdir(rib_files_directory_path)
	
	# iterate through all rib files, create PyStream events
	for rib_file in rib_files:
    	
    	# create stream object with provided file
    	epoch = rib_file.split(".")[3]
    	stream = pybgpstream.BGPStream(data_interface="singlefile")
    	stream.set_data_interface_option("singlefile", "rib-file", "{}/{}".format(rib_files_directory_path, rib_file))
    	results[epoch] = {
    		"prefixes": [],
    		"ases": [],
    		"originAses": {}
    	}
    	
    	# process stream for prefixes & ASES
    	for index, element in enumerate(stream):
    	
    		print("processing index = {}".format(index))
    		
    		# get the prefix
    		pfx = element.fields["prefix"]
    		
    		# get the list of ASes in the AS path
    		ases = element.fields["as-path"].split(" ")
    		
    		# get the origin ASn (rightmost)
    		origin = ases[-1]
    		
    		# handle case of origin as being a set
    		if type(origin) == set:
    		
    			# convert set to list type
    			origin = list(origin)
    			
    			# remove old set from ases
    			ases.remove(ases[-1])
    			
    			# append origins back to list
    			ases.extend(origin)
    			
    		# filter for unique ases
    		ases = list(set(ases))
    		
    		# add this unique prefix
    		results[epoch]["prefixes"].append(pfx)
    			
    		# extend new ases to list
    		results[epoch]["ases"].extend(ases)
    		
    		# handing for unique prefixes/ases
    		#if index == 0:
    			
    			# add this unique prefix
    			#results[epoch]["prefixes"].append(pfx)
    			
    			# extend new ases to list
    			#results[epoch]["ases"].extend(ases)
    			
    		#else:
    		
    			# fetch previous values for origin and pfx
    			#previousPrefix = results[epoch]["prefixes"][-1]
    			
    			# is this prefix unique
    			#if pfx != previousPrefix:
    			
    				# add this unique prefix
    				#results[epoch]["prefixes"].append(pfx)
    				
    			# extend new ases to list
    			#results[epoch]["ases"].extend(ases)
    				
    	# filter for unique ases via set/list conversion
    	results[epoch]["prefixes"] = list(set(results[epoch]["prefixes"]))
    	results[epoch]["ases"] = list(set(results[epoch]["ases"]))		
