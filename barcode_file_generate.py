import sys
sys.path.append('/san/home/yunfeng.hu/Chemistry/PythonCode/')

import pandas as pd 
import os
import numpy as np 
from generate_rv_complex import *
from numpy.linalg import norm
from numpy import inf
from generate_rv_complex import *
import csv
import argparse


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputPath')
	parser.add_argument('--outputPath')
	parser.add_argument('--inputFile')
	args = parser.parse_args()

	os.chdir(args.outputPath)


	# load data 
	df = pd.read_csv(args.inputPath + args.inputFile)
	targetwindow = df['Snapshot'].unique()
	index = args.inputFile.split('-')[1]
	index = index.replace('.csv', '')


	with open(args.outputPath + index +'_barcode.csv','w') as fout:
		csv.writer(fout).writerow(['Snapshot', 'Dimension', 'Filtration', 'Birth', 'Death', 'Generator', 'Terminator', 'Flag'])	
		for targetsnapshot in targetwindow:
			dfTempt = df[df['Snapshot']==targetsnapshot]
			points = np.array(dfTempt.iloc[:,3:6])
			# Cutoff = cutoff(points)
			rips,m,dgms = generate_rv_complex(points,3)
			for i,dgm in enumerate(dgms):
				if i<=2:
					for s in dgm:
						if s.death != np.inf:
							birthGen = list(rips.__getitem__(s.data))
							deathGen = list(rips.__getitem__(m.pair(s.data)))
							if set(birthGen).intersection(set(deathGen)) == set(birthGen):
								flag = 1
							else:
								flag = 0
							csv.writer(fout).writerow([targetsnapshot, i, s.data, s.birth, s.death, birthGen, deathGen, flag])
						else:
							csv.writer(fout).writerow([targetsnapshot, i, s.data, s.birth, 1, list(rips.__getitem__(s.data)), 1, 0])
				else: continue


if (__name__ == '__main__'):
	main()
