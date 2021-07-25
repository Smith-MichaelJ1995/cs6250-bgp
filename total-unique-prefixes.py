# Task 1 Responses:
# 1. The total number of prefixes and ASes are increasing in paralell over time. The rate of growth for both prefixes and ASes appears to be steady and consistiently linear. From 2018, it appears that both graphs are beginning to reflect an exponential growth pattern.

# 2. To solve this challenge, I calculated the average number of unique prefixes across OriginAses in an epoch. I computed this metric for all years from 2013-2021. The findings showed the following: [(2013, 10.50), (2014, 10.89), (2015, 11.03), (2016, 11.57), (2017, 12.04), (2018, 12.33), (2019, 12.95), (2020, 13.25), (2021, 13.47)]. I have discovered that the majority of origin ASes have an increased number of total unique advertized prefixes over time.

# 3.   
###

import os
import datetime
import json

# read in files from filesystem
def read_from_filesystem():
   with open('task1partB-results.json', 'r') as f:
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
   


      

