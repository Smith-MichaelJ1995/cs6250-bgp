# Import the pybgpstream library and any graphing library here
import pybgpstream
import os
import datetime
import json
import numpy
from matplotlib import pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF 


# read in files from filesystem
def read_from_filesystem():
   with open('task2-results.json', 'r') as f:
      return f.read()
      
def write_to_filesystem(results):
	with open('task2-results.json', 'w') as fp:
		json.dump(results, fp)
		

def generate_results():

   # Replace the contents of this cell with your code for Task 1 part A
   results = {}
   notebook_path = os.path.abspath("task2.py")
   rib_files_directory_path = os.path.join(os.path.dirname(notebook_path), "rib_files")
   rib_files = os.listdir(rib_files_directory_path)
	
   # iterate through all rib files, create PyStream events
   for rib_file in rib_files:
   
      #print("Processing New File: {}".format(rib_file))
    	
      # create stream object with provided file
      epoch = rib_file.split(".")[3]
      stream = pybgpstream.BGPStream(data_interface="singlefile")
      stream.set_data_interface_option("singlefile", "rib-file", "{}/{}".format(rib_files_directory_path, rib_file))
      results[epoch] = {
       "originAses": {}
      }
    	
      # process stream for prefixes & ASES
      for index, element in enumerate(stream):
    		
         #print("processing index = {}".format(index))
    			
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
    				
         # filter for unique ases
         ases = list(set(ases))
         
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
#results = generate_results()
#write_to_filesystem(results)

results = json.loads(read_from_filesystem())
years = ["2013","2014","2015","2016","2017","2018","2019","2020","2021"]
plots = []

# traverse through all timestamps in sequential order
for stamp in sorted(results.keys()):
   
   # fetch all path lengths for each as
   # asOrigins = list(results[stamp]["originAses"].keys())
   asPathLengths = list(results[stamp]["originAses"].values())
   
   # instantiate ecdf object
   ecdf = ECDF(asPathLengths)
   
   # configure this plot data
   plotObject, = plt.plot(ecdf.x, ecdf.y, lw = 2)
   
   # append plot object for future use
   plots.append(plotObject)
   
# generate plot
plt.legend(plots, years)
plt.xlabel("Shortest Path Length", size=14)
plt.ylabel("Prob", size = 14)
   
# print plot
plt.show()


   
   






   	
		
		
		
		
		
		
		
		

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
