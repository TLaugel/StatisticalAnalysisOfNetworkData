####################################################
# compute the SVD of the matrix and save a matrix of rank N (define in the script)
####################################################
import numpy as np
import pandas
import os
import time
import sys
import gzip
import sys
import operator 

if len(list(sys.argv)) > 1 :
  sigma = float(sys.argv[1])
else :
  sigma = .1

maxDate ="2000-12-31"
### rank of the matrix return : lower rank approximation
N = 1000

###Input files : covariance matrix, list of movies, test data
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'

Covin = foutCov = path+'CovMatrix_'+maxDate+'_%f.txt' % sigma
Cov = np.loadtxt(Covin, delimiter = ',')

fin = path+'dbEffects'+maxDate+'_%f.txt' % sigma
df = pandas.read_csv(fin,sep="\t",encoding="utf8")

listMovies = df.groupby('movieID')['movieID'].max().tolist()
listUsers = df.groupby('userID')['userID'].max().tolist()


print "Decomposing SVD for sigma=%f" % sigma
import datetime
import time
timestart =  time.time()
U, s, V = np.linalg.svd(Cov,full_matrices=True)
print  time.time()-timestart 
dim  = s.shape[0]
s[(N +1):] = np.zeros(dim-N -1)
S = np.diag(s)

print "Reconstructing the matrix"
timestart =  time.time()
res = U.dot(S.dot(V.transpose())) #there is a faster way to reconstruct it : block matrix
print  time.time()-timestart 

print "Saving the matrix"
timestart =  time.time()
compressMat = path+'compressMat_'+maxDate+'_%f.txt' % sigma
np.savetxt(compressMat,res,delimiter=',')
print  time.time()-timestart 
	
	
