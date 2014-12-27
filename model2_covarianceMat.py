#######################
# model part 2: computation of covariance and weight matrices
#########################

import numpy, pandas
import os
import time
import sys
import gzip
import sys
#maxdate of the previous file
if len(list(sys.argv)) > 1 :
  maxDate = sys.argv[1]
else :
  maxDate = "2002-12-31"



####input is the output dataframe of the script model.py 
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'
fin = path+'dbEffects'+maxDate+'.txt'
df = pandas.read_csv(fin,sep="\t",encoding="utf8")

###functions

#rbarSerie : for a user, creates the matrix of size nbMovies^2 with M[i,j]=weight_user*rbar_user[i]*rbar_user[j]
def rbarSerie(user):
    M = df[["movieID", "centeredRating"]][df["userID"] == user] #je prends films id et rating centered pour mon user
    M = pandas.merge(moviesall,M, left_on='movieID', right_on='movieID', how='left') #left join on list of unique movies
    M = M["centeredRating"].fillna(0) #replace NaN from the left join by zeros and keep only centeredRating : this is now a Serie of size nbMovies
    M = numpy.asmatrix(M.as_matrix()) #convert to an array then a matrix to get the transpose(not working for a 1 dimension vector with array format)
    Mat = weight[user] * M.T * M
    return M

def onezeromat(matrix):
    return numpy.asmatrix(numpy.where(matrix>0, 1, 0)) 



####Parameters
nbMovies = len(pandas.Series(df["movieID"].values.ravel()).unique())
UCnt = df.groupby('userID').agg(['count'])["rating"] #how many movies each user
UCnt = UCnt.ix[:,0]
weight = 1.0/UCnt #vector containing one weight for each user
moviesall = df.groupby('movieID')[['movieID']].max()

###Matrices and Noise matrices initialization
Cov = numpy.asmatrix( numpy.zeros((nbMovies, nbMovies))) 
Wgt = Cov.copy()
NoiseCov = numpy.asmatrix( numpy.zeros((nbMovies, nbMovies)))  #noise matrix
NoiseWgt = NoiseCov

print "I am here"
###loop on users: for each user, we compute its corresponding Cov and Wgt matrices and aggregate them to the others
for user in pandas.Series(df["userID"].values.ravel()).unique():
    rbarMatrix = rbarSerie(user) #matrix of size nbMovies^2 #weight[user] * rbar.T * rbar # matrix size nbMovies^2
    euMatrix = onezeromat(rbarMatrix) #idem with 1 instead of the ratings #weight[user] * eu.T * eu #idem
    Cov = Cov + rbarMatrix #let's sum baby
    Wgt = Wgt + euMatrix

Cov = Cov + NoiseCov
Wgt = Wgt + NoiseWgt


###Cleaning the covariance matrix
beta = 0  # NB :  the paper states that they used different values of beta for the diagonal and for the rest> to consider
Cov = Cov + beta * Cov.mean()
Wgt = Wgt + beta * Wgt.mean()
Cov = numpy.divide(Cov,Wgt) #division term by term

###Ouput files : we save each matrix in a separate txt file
#~ path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
foutCov = path+'CovMatrix'+maxDate+'.txt'
#foutWgt = path+'WgtMatrix'+maxDate+'.txt'
numpy.savetxt(foutCov,Cov,delimiter=',')
#numpy.savetxt(foutWgt,Wgt,delimiter=',')
