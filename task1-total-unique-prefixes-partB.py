import os
import datetime
import json

# read in files from filesystem
def read_from_filesystem():
   with open('task1-results.json', 'r') as f:
      return f.read()
		
# ave unique prefixes by year
# averageUniquePrefixesByYear = {}

# fetch results dict from the filesystem
results = json.loads(read_from_filesystem())

# traverse through all keys, sorted in timestamp order
for epoch in sorted(results.keys()):

   print("Processing new epoch = {}".format(epoch))

   # placeholder for average
   avg = 0
   num = 0
   denom = len(results[epoch]["originAses"].keys())
		
   # list origins/prefixes
   for originAs, prefixes in results[epoch]["originAses"].items():
      num += len(prefixes)
      
      
   # calculate average total unique prefixes
   avg = num / denom
   
   print("avg = {}".format(avg))

   # stage result for this prefix
   # averageUniquePrefixesByYear[epoch] = avg
   


      

