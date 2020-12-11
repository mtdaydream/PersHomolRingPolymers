# import packages 
import sys
#sys.path.append('/san/home/yunfeng.hu/PythonCode/')
import pandas as pd 
import os
import numpy as np 
import collections
from operator import *


# set path 
inputPath = '/san/home/yunfeng.hu/Chemistry/all_64rep_barcode_20170714/'
outputPath = '/san/home/yunfeng.hu/Chemistry/all_64rep_bettiseq_20170714/'
os.chdir(outputPath)

# laod files 

## stable files 
files = os.listdir(inputPath)
bettiSeq = np.linspace(0,1.5,601)

## convert barcode to betti sequence

for file in files:	
	bettiSeqDict = collections.defaultdict(list)
	df = pd.read_csv(inputPath + file)
	df.loc[df['Terminator'] == '1', 'Death'] = 1.5
	snapshots = df['Snapshot'].unique()
	for snapshot in snapshots:
		dictname = file.split('_')[0] + '_' + str(snapshot)
		dfSnapshot = df[df['Snapshot']==snapshot]
		bettiSeqDim = []
		for dim in range(2):
			dfSnapshotDim = dfSnapshot[dfSnapshot['Dimension'] == dim]
			dfSnapshotDim = np.array(dfSnapshotDim[['Birth', 'Death']])
			bettiSeqTempt = np.zeros(601)
			for dimlen in range(len(dfSnapshotDim)):
				bettiSeqDimTempt = np.heaviside(bettiSeq - dfSnapshotDim[dimlen,0], 0) - np.heaviside(bettiSeq - dfSnapshotDim[dimlen,1], 0)
				bettiSeqTempt += bettiSeqDimTempt
				bettiSeqTempt[0] = 64
			bettiSeqDim.append(bettiSeqTempt)
		bettiSeqDim = np.array(bettiSeqDim)
		bettiSeqDict[dictname].append(bettiSeqDim)
	savename = file.replace('barcode.csv', 'BettiSeq.npy')
	np.save(savename, bettiSeqDict)

