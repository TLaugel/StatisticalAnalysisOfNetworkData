#######################
# model part 2: computation of covariance and weight matrices
#########################

import numpy, pandas
import os
import time
import sys
import gzip
import sys

if len(list(sys.argv)) > 1 :
  sigma = float(sys.argv[1])
else :
  sigma = .1
maxDate= "2000-12-31"
maxDateStr= "2000-12-31"


####input is the output dataframe of the script model.py 
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'

fin = path+'dbEffects'+maxDate+'_%f.txt' % sigma
df = pandas.read_csv(fin,sep="\t",encoding="utf8")
VarKept = ['movieID','userID','centeredRating']
VarDel =  [el for el in df if not el in VarKept]
df.drop(VarDel, axis=1, inplace=True)

###functions
from scipy.sparse import csc_matrix as sparseM
def rbarSerie(user):
    M = df.loc[df.index==user,["movieID", "centeredRating"]] 
    M = pandas.merge(moviesall,M, left_on='movieID', right_on='movieID', how='left') #left join on list of unique movies
    M = M["centeredRating"].fillna(0) #replace NaN from the left join by zeros and keep only centeredRating : this is now a Serie of size nbMovies
    M = sparseM(M)
    Mat = weight[user] * M.transpose().dot(M)
    return Mat 

def onezeromat(matrix):
    return numpy.asmatrix(numpy.where(matrix>0, 1, 0)) 

####Parameters
nbMovies = len(pandas.Series(df["movieID"].values.ravel()).unique())
UCnt = df.groupby('userID').agg(['count'])["movieID"] #how many movies each user
UCnt = UCnt.ix[:,0]
weight = 1.0/UCnt #vector containing one weight for each user
moviesall = df.groupby('movieID')[['movieID']].max()

###Matrices and Noise matrices initialization
Cov = numpy.asmatrix( numpy.zeros((nbMovies, nbMovies))) 
Wgt = Cov.copy()

print "I am here"
###loop on users: for each user, we compute its corresponding Cov and Wgt matrices and aggregate them to the others
i = 0
import datetime
import time
timestart =  time.time()
df.set_index(['userID'], inplace = True) #index to speed-up the computation time
for user in pandas.Series(df.index.values.ravel()).unique():
	rbarMatrix = rbarSerie(user) #matrix of size nbMovies^2 #weight[user] * rbar.T * rbar # matrix size nbMovies^2
	Cov += rbarMatrix.todense()
	Wgt += numpy.greater(rbarMatrix.todense(),0) 
print  time.time()-timestart 


##No Noise for now ... (Memory issue)
print "adding noise"
noise = numpy.random.normal(0,sigma,(nbMovies, nbMovies))
for i in range(nbMovies): #for having a symetrical noise : the covariance matrix must be symetrical
	for j in range(i,nbMovies):
		noise[i,j] = noise[j,i]
Cov += noise
noise = numpy.random.normal(0,sigma,(nbMovies, nbMovies))
for i in range(nbMovies): #for having a symetrical noise : the covariance matrix must be symetrical
	for j in range(i,nbMovies):
		noise[i,j] = noise[j,i]
Wgt += numpy.random.normal(0,sigma,(nbMovies, nbMovies))


###Cleaning the covariance matrix
print "cleaning the covariance matrix"
beta = 0  # NB :  the paper states that they used different values of beta for the diagonal and for the rest> to consider
Cov += beta * Cov.mean()
Wgt += beta * Wgt.mean()
Cov = numpy.divide(Cov,Wgt) #division term by term

###Ouput files : we save each matrix in a separate txt file
print "save the matrices"
foutCov = path+'CovMatrix_'+maxDate+'_%f.txt' % sigma
#~ foutWgt = path+'WgtMatrix_'+maxDate+'_%f.txt' % sigma #we don't need to save it, it is useless for the next scripts
numpy.savetxt(foutCov,Cov,delimiter=',')
#~ numpy.savetxt(foutWgt,Wgt,delimiter=',')
