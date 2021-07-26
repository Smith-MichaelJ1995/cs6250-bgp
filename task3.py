# Import the pybgpstream library and any graphing library here
import pybgpstream
import os
import datetime
import json
from matplotlib import pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF


# read in files from filesystem
def read_from_filesystem():
   with open('task1-results.json', 'r') as f:
      return f.read()
      
def write_to_filesystem(results):
	with open('task2-results.json', 'w') as fp:
		json.dump(results, fp)
		
def generate_task3_results():

   # Replace the contents of this cell with your code for Task 1 part A
   notebook_path = os.path.abspath("task3.py")
   update_files_blackholing_directory_path = os.path.join(os.path.dirname(notebook_path), "update_files_blackholing")
   update_files = os.listdir(update_files_blackholing_directory_path)
   
   # prefix placeholders with IPV4 vuln
   vulnPrefixes = {}
   
   # iterate through all rib files, create PyStream events
   for update_file in update_files:
    	
      # create stream object with provided file
      epoch = update_file.split(".")[3]
      stream = pybgpstream.BGPStream(data_interface="singlefile")
      stream.set_data_interface_option("singlefile", "upd-file", "{}/{}".format(update_files_blackholing_directory_path, update_file))
    	
      # process stream for prefixes & ASES
      for index, element in enumerate(stream):
      
         # determine element type
         type = element.type
               
         # determine time
         time = element.time
         
         # handle based on event type
         if type == "A":
            
            # get the prefix
            pfx = element.fields["prefix"]
         
            # get the peer address
            peerIP = element.peer_address
            
            # fetch communities for given record
            if 'communities' in element.fields:
          
               # extract communities
               communities = element.fields['communities']
               
               # does element belong to ipv4 blackhole community
               if len(communities) > 0:
               
                  # create container for key
                  key = "{}=={}".format(pfx, peerIP)
               
                  # append start time
                  vulnPrefixes[key] = {"start": time}
            
         elif type == "W":
         
            # create container for key
            key = "{}=={}".format(pfx, peerIP)
                  
            # handle if we're listening for this withdrawl
            if key in vulnPrefixes.keys() and vulnPrefixes[key]["start"] < time and len(vulnPrefixes[key].keys()) == 1:
               
               # append start time
               vulnPrefixes[key]["end"] = time
               vulnPrefixes[key]["duration"] = vulnPrefixes[key]["end"] - vulnPrefixes[key]["start"]
               
            else:
               pass
            
   
   #break         
   return vulnPrefixes   
   
   
def filterForPrefixDurations(vulnPrefixes):

   vulnPrefixDurations = []

   # traverse through all vulns
   for vulnPrefix in vulnPrefixes.keys():
   
     # check for empty start event
     if len(vulnPrefixes[vulnPrefix].keys()) > 1:
        vulnPrefixDurations.append(vulnPrefixes[vulnPrefix]["duration"]) 
      
   # return vulnerPrefixDurations
   return vulnPrefixDurations  
   

# fetch results
vulnPrefixes = generate_task3_results()

# find durations
durationData = filterForPrefixDurations(vulnPrefixes)

   		
# instantiate ecdf object
ecdf = ECDF(durationData)
   		
# configure this plot data
plt.plot(ecdf.x, ecdf.y, lw = 2)
plt.title("ECDF of Blackhole Duration & Probability", size=14)
plt.xlabel("Duration", size=14)
plt.ylabel("Prob", size = 14)
   	
# print plot
plt.show()


