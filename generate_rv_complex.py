
from scipy.spatial.distance import pdist
import dionysus as d 
def generate_rv_complex(PointsArray, Dimension):
	dists = pdist(PointsArray)
	# adjacentDist = [norm(PointsArray[i,:] - PointsArray[i+1,:]) for i in range(len(PointsArray)-1)]
	Alpha = max(dists)
	rips = d.fill_rips(dists, Dimension, Alpha)
	m = d.homology_persistence(rips)
	dgms = d.init_diagrams(m, rips)
	return rips, m, dgms
