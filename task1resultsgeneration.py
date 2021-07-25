# Import the pybgpstream library and any graphing library here
import pybgpstream
import os
import datetime
import json
from matplotlib import pyplot as plt

def generate_results():

   # Replace the contents of this cell with your code for Task 1 part A
   results = {}
   notebook_path = os.path.abspath("main.py")
   rib_files_directory_path = os.path.join(os.path.dirname(notebook_path), "rib_files")
   rib_files = os.listdir(rib_files_directory_path)
	
   # iterate through all rib files, create PyStream events
   for rib_file in rib_files:
   
      print("Processing New File: {}".format(rib_file))
    	
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
         if "{" in origin:
         
            print("type of origin is a set")
            print("origin = {}".format(origin))
         
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
            
            print("re-formatted origin = {}".format(origin))
            print("re-formatted ases = {}".format(ases))
            print("")
            # exit()
    				
         # filter for unique ases
         ases = list(set(ases))
    			
         # add this unique prefix
         results[epoch]["prefixes"].append(pfx)
    				
         # extend new ases to list
         results[epoch]["ases"].extend(ases)
    			
         # handle originAses if it's unique
         if origin not in results[epoch]["originAses"].keys():
            results[epoch]["originAses"][origin] = [pfx]
         else:
            if pfx not in results[epoch]["originAses"][origin]:
               results[epoch]["originAses"][origin].append(pfx)
    				
      # filter for unique ases via set/list conversion
      results[epoch]["prefixes"] = list(set(results[epoch]["prefixes"]))
      results[epoch]["ases"] = list(set(results[epoch]["ases"]))
     
   return results	

# print originAses
def print_results(results):

   # traverse through all keys, sorted in timestamp order
   for epoch in sorted(results.keys()):
		
      # list origins/prefixes
      for originAs, prefixes in results[epoch]["originAses"].items():
         print("originAs = {}".format(originAs))
         print("prefixes = {}".format(prefixes))
         print("###############################")
         
def write_to_filesystem(results):
	with open('task1-results.json', 'w') as fp:
		json.dump(results, fp)

results = generate_results()
write_to_filesystem(results)
