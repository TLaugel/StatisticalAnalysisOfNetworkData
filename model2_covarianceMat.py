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
  maxDate = "2000-12-31"



####input is the output dataframe of the script model.py 
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'
fin = path+'dbEffects'+maxDate+'.txt'
df = pandas.read_csv(fin,sep="\t",encoding="utf8")
VarKept = ['movieID','userID','centeredRating']
VarDel =  [el for el in df if not el in VarKept]
df.drop(VarDel, axis=1, inplace=True)

###functions
from scipy.sparse import csc_matrix as sparseM
def rbarSerie(user):
    M = df.loc[df.index==user,["movieID", "centeredRating"]] #je prends films id et rating centered pour mon user /!\ df doit etre indexee seulement selon userID
    M = pandas.merge(moviesall,M, left_on='movieID', right_on='movieID', how='left') #left join on list of unique movies
    
    M = M["centeredRating"].fillna(0) #replace NaN from the left join by zeros and keep only centeredRating : this is now a Serie of size nbMovies
    M = sparseM(M)
    Mat = weight[user] * M.transpose().dot(M) #I think it was M*M.T in the paper, buuut our array are line and not 
    return Mat #why don't you return Mat (it was M before, I assume it was a mistake)

def onezeromat(matrix):
    return numpy.asmatrix(numpy.where(matrix>0, 1, 0)) 

#~ def onezeroAux(x):
	#~ return int(x>0)
#~ oneZero= numpy.vectorize(onezeroAux, otypes=[numpy.int])

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
df.set_index(['userID'], inplace = True) #small improvment : a bit faster...
for user in pandas.Series(df.index.values.ravel()).unique():
	rbarMatrix = rbarSerie(user) #matrix of size nbMovies^2 #weight[user] * rbar.T * rbar # matrix size nbMovies^2
	Cov += rbarMatrix.todense() #let's sum baby
	Wgt += numpy.greater(rbarMatrix.todense(),0) #j'avais fait une connerie ici...
	#~ i += 1
	#~ if i > 1 :
		#~ break
print  time.time()-timestart 


##No Noise for now ... (Memory issue)
print "adding noise"
sigma = .1
Cov += numpy.random.normal(0,sigma,(nbMovies, nbMovies))
Wgt += numpy.random.normal(0,sigma,(nbMovies, nbMovies))


###Cleaning the covariance matrix
print "cleaning the covariance matrix"
beta = 0  # NB :  the paper states that they used different values of beta for the diagonal and for the rest> to consider
Cov += beta * Cov.mean()
Wgt += beta * Wgt.mean()
Cov = numpy.divide(Cov,Wgt) #division term by term

###Ouput files : we save each matrix in a separate txt file
print "save the matrices"
#~ path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
foutCov = path+'CovMatrix_'+maxDate+'.txt'
foutWgt = path+'WgtMatrix_'+maxDate+'.txt'
numpy.savetxt(foutCov,Cov,delimiter=',')
numpy.savetxt(foutWgt,Wgt,delimiter=',')
