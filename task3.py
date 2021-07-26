# Import the pybgpstream library and any graphing library here
import pybgpstream
import os
import datetime
import json
from matplotlib import pyplot as plt


# read in files from filesystem
def read_from_filesystem():
   with open('task1-results.json', 'r') as f:
      return f.read()
      
def write_to_filesystem(results):
	with open('task2-results.json', 'w') as fp:
		json.dump(results, fp)
		

def generate_results():

   # Replace the contents of this cell with your code for Task 1 part A
   results = {}
   notebook_path = os.path.abspath("task3.py")
   update_files_blackholing_directory_path = os.path.join(os.path.dirname(notebook_path), "update_files_blackholing")
   update_files = os.listdir(update_files_blackholing_directory_path)
   
   #print(update_files)
   #exit()
   
   # iterate through all rib files, create PyStream events
   for update_file in update_files:
   
      #print("Processing New File: {}".format(rib_file))
    	
      # create stream object with provided file
      epoch = update_file.split(".")[3]
      stream = pybgpstream.BGPStream(data_interface="singlefile")
      stream.set_data_interface_option("singlefile", "upd-file", "{}/{}".format(update_files_blackholing_directory_path, update_file))
      #results[epoch] = {
      # "originAses": {}
      #}
    	
      # process stream for prefixes & ASES
      for index, element in enumerate(stream):
    		
         print("processing index = {}".format(index))
         print("processing element = {}".format(element))
         exit()
    			
         # get the list of ASes in the AS path
         ases = element.fields["as-path"].split(" ")
    			
         # get the origin ASn (rightmost)
         origin = ases[-1]
    			
         # handle case of origin as being a set
         if "{" in origin:
         
            #print("type of origin is a set")
            #print("origin = {}".format(origin))
         
            # remove old set from ases
            ases.remove(origin)
    			
            # remove paren's from origin string
            origin = origin.strip("{")
            origin = origin.strip("}")
            
            # split based on commas
            origin = origin.split(",")
    				
            # append origins back to list
            ases.extend(origin)
            
            # hold right-most origin value
            origin = origin[-1]
            
            #print("re-formatted origin = {}".format(origin))
            #print("re-formatted ases = {}".format(ases))
            #print("")
    				
         # filter for unique ases
         ases = list(set(ases))
         
         #print("###########")
         #print("origin = {}".format(origin))		
         #print("ases = {}".format(ases))
         
         # handle originAses if it's unique
         if origin not in results[epoch]["originAses"].keys():
         
            # set default shortest path length for originAs
            results[epoch]["originAses"][origin] = len(ases)
            
         else:
         
            # fetch current shortest path length for originAs
            currentShortestPathLength = results[epoch]["originAses"][origin]
            asesLength = len(ases)
            
            # determine if we've found a shorter path for this AS
            if asesLength < currentShortestPathLength:
            
               # stage this value
               results[epoch]["originAses"][origin] = asesLength 
               
   return results    
	
# invoke function, generate results, stage to filesystem	
results = generate_results()
# write_to_filesystem(results)
   	
		
		
		
		
		
		
		
		

# fetch results dict from the filesystem
#results = json.loads(read_from_filesystem())

# traverse through all epochs in order
#for epoch in sorted(results.keys()):

   # fetch all unique originAses within this epoch
#   asesInEpoch = results[epoch]['ases']
   
#   print("asesInEpoch = {}".format(asesInEpoch))
#   exit()
   
   # return all ases for this
#   for path in asesInEpoch:
   
      # extrapolate the originAs
#      originAsInPath = path[-1]
      
      # extract prior originAs ID
#     distinctOriginDataSet = results[epoch]["originAses"][originAsInPath]
      
      # determine if this originAs has been converted to a dict yet
#       if isinstance(distinctOriginDataSet, list):
      
         # store dict in place of old integer value
#         results[epoch]["originAses"][originAsInPath] = { 
#            "uniqueOriginAsPrefixes": distinctOriginDataSet,
#            "paths": [path]
#         }
         
#      else:
      
#        print("originAsInPath = {}".format(originAsInPath))
#         print(results[epoch]["originAses"][originAsInPath])
#         exit()
      
         # place the new value
#         results[epoch]["originAses"][originAsInPath]["paths"].append(path)
         

# traverse through all originAses to validate output
#for uniqueAses in results[epoch]["originAses"]:
   
#   print("uniqueAs = {}".format(uniqueAses["originAs"]))
#   print("paths = {}".format(uniqueAses["paths"]))
   # print("paths = {}".format(uniqueAses["paths"]))
#   print("#####")

# write new updated paths to the filesystem        
#write_to_filesystem(results)
