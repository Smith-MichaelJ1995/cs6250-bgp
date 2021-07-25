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

# universe of originAses
universeOriginAses = []
universeOriginAsesWithChangeTotals = []

# sort keys in timestamp order
chronologicallySortedKeys = sorted(results.keys())
reverseChronologicallySortedKeys = sorted(results.keys(), reverse=True)

# traverse through all keys, sorted in timestamp order
for epoch in chronologicallySortedKeys:

   print("Processing new epoch = {}".format(epoch))
   
   # include all unique originAses from this epoch
   universeOriginAses.extend(results[epoch]["originAses"].keys())
      

# filter for OriginAs duplicates, we must have unique values
universeOriginAses = list(set(universeOriginAses))

# remove empty string character
print("total universeOriginAses = {}".format(len(universeOriginAses)))
input("Press Enter..")

# now that we have all unique originAses (across entire timespan 2013-2021), find percent raise for each
for index, originAs in enumerate(universeOriginAses):

   if index != 0:

      # notate the originAs we're processing
      print("index = {}, originAs = {}".format(index, originAs))
      print("originAs = {}".format(originAs))

      # create placeholder for start epoch
      startUniquePrefixesCount = 0
      endUniquePrefixesCount = 0
   
      #find first appearance for this epoch
      for epoch in chronologicallySortedKeys:
         if originAs in results[epoch]["originAses"].keys():
            startUniquePrefixesCount = len(results[epoch]["originAses"][originAs])
            break
   
      #find the last appearance for this epoch 
      for epoch in reverseChronologicallySortedKeys:
         if originAs in results[epoch]["originAses"].keys():
            endUniquePrefixesCount = len(results[epoch]["originAses"][originAs])
            break
      
      # calculate percent change
      changeInPrefixes = endUniquePrefixesCount - startUniquePrefixesCount
      totalPercentageIncrease = (changeInPrefixes / startUniquePrefixesCount) * 100
      #print("total % increase = {}".format(totalPercentageIncrease))
   
      # save results to new placeholder
      universeOriginAsesWithChangeTotals.append({"originAs": originAs, "pct-change": totalPercentageIncrease})

# show resulting originAses with highest percentage change
print(sorted(universeOriginAsesWithChangeTotals, key = lambda item: item['pct-change'], reverse=True))
      

