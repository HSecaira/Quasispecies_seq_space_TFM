"""
Script that maps the nodesID of subnetworks to the nodesID of the Grand Network
"""

import numpy as np;
import os, sys;

####################################################################
# Some functions
def loadExperimentalConditions(fIn):
	"""
	FUnction that reads all the names of experimental conditions in a file 
	Inputs: 
		fIn: file containing the names of the experimental conditions 
	Outputs:
		expConds: list of strings, containing the experimental conditions 
	"""

	# List to store the names
	expConds = []

	# Iterate over the file
	with open(fIn, "r") as fIn_:
		for line in fIn_:
			expConds.append(str(line.strip()))

	return expConds

def loadEdges(fIn):
	"""
	Function that reads the edges from an edges file generated by Luiño's Grand Network code
	Inputs:
		fIn: file containing the edges of the network
	Outputs: 
		edges: list of lists containing the edges
	"""

	# Declare structures
	edges = []

	# Iterate over file
	with open(fIn, "r") as fIn_:
		for line in fIn_:
			sourceEdge = int(line.strip().split(", ")[0])
			sinkEdge = int(line.strip().split(", ")[1])
			edges.append([sourceEdge, sinkEdge])

	return edges

def mapEdges(newEdges, oldEdges):
	"""
	Function taht maps oldEdges to New edges 
	Inputs:
		newEdges: list of lists of ints containing the new edges
		oldEdges: list of lists of ints containing the old edges
	Outputs: 
		mapIDs: dictionary whose values are the oldNodesID and values are the newNodesID
	"""

	# Declare structures
	mapIDs = {}
	temp = {}

	# oldEdges and newEdges are both sortered, so a simple mapping with
	# a for loop will be enough
	# First loop for connections/edges
	for i in range(len(oldEdges)):

		# Get the connections
		connectionOld = oldEdges[i]
		connectionNew = newEdges[i]
		# Get the source and sink nodes
		sourceNodeOld = connectionOld[0]
		sourceNodeNew = connectionNew[0]
		sinkNodeOld = connectionOld[1]
		sinkNodeNew = connectionNew[1]

		# Add to dictionary containing the mapping
		if sourceNodeOld not in temp.keys():
			temp[sourceNodeOld] = sourceNodeNew

		if sinkNodeOld not in temp.keys():
			temp[sinkNodeOld] = sinkNodeNew

	# Order dictionary by newIDs
	mapIDs = dict(sorted(temp.items(), key = lambda x:x[1]))

	return mapIDs

def saveMapping(fOut, mapIDs):
	"""
	Function that saves the mapping of oldIDs to newIDs into a file
	Inputs:
		fOut: file in which we want to save the mapping
		mapIDs: dictionary whose values are the oldNodesID and values are the newNodesID
	Outputs: none
	"""
	with open(fOut, "w") as fOut_:

		# Write header
		fOut_.write("#OldNodeID,NewNodeID\n")

		# Iterate over dictionary
		for old, new in mapIDs.items():
			fOut_.write(str(old) + "," + str(new) + "\n")


####################################################################

# Declare paths
dataPathIn = "/home/henry/Downloads/Jae_Beca/NGS_all_seqs/GNR/Topology/Experiments/"
dicFolder = {}; 
dicFolder["r1"] = "Reg1"; 
dicFolder["r2"] = "Reg2"; 
dicFolder["r3"] = "Reg3"; 

# Declare region
reg = "r1"
dataPathIn_ = dataPathIn + dicFolder[reg] + "_experiments/" + "SubNetworks/"

# Load experimental conditions
fInExpConds = os.path.join(dataPathIn_, "filesNames" + ".csv")
# Load the names of the experimental conditions
expConds = loadExperimentalConditions(fInExpConds)

# Iterate over experimental conditions
for experimentalCondition in expConds:
	print("At", experimentalCondition, "\n")
	# Redefine paths
	dataPathIn__ = dataPathIn_ + experimentalCondition + "/"
	dataPathOut__ = dataPathIn__

	# Load new Edges file
	fInNewEdges = os.path.join(dataPathIn__, "edges" + ".csv")
	newEdges = loadEdges(fInNewEdges)

	# Load old edges paths
	fInOldEdges = os.path.join(dataPathIn__, "oldEdges" + ".csv")
	oldEdges = loadEdges(fInOldEdges)

	# Map newEdges to oldEdges
	mapIDs = mapEdges(newEdges, oldEdges)

	# Save mapping
	fOut = os.path.join(dataPathOut__, "mapNodesIDs" + ".csv")
	saveMapping(fOut, mapIDs)
	print("\tMapping done and save into a file\n")







