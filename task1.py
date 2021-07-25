# Import the pybgpstream library and any graphing library here
import pybgpstream
import os
import datetime
import json
from matplotlib import pyplot as plt
			
	
def read_from_filesystem():
	with open('task1partA-results.json', 'r') as f:
		return f.read()

def write_to_filesystem():
	with open('task1partA-results.json', 'w') as fp:
		json.dump(results, fp)
		
def build_plotlib_chart(results, key, title, xlabel, ylabel):
	
	# create datastructure for prefixes plot data
	xAxis = ["2013","2014","2015","2016","2017","2018","2019","2020","2021"]
	yAxis = [] 
	
	# traverse through all keys, sorted in timestamp order
	for epoch in sorted(results.keys()):
	
		# build chart data
		yAxis.append(len(results[epoch][key]))
		
	# create plot placeholder objects with labels
	plt.plot(xAxis, yAxis)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	
	
	# display the plots
	plt.show()

# read results
results = json.loads(read_from_filesystem())

# build chart
build_plotlib_chart(results, "prefixes", "Total Unique Prefixes Over Time", "Date", "Total Unique Prefixes")
build_plotlib_chart(results, "ases", "Total Unique ASes Over Time", "Date", "Total Unique ASes")


