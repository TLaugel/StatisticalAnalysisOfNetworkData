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
  maxDate = time.strptime(sys.argv[1],"%Y-%m-%d")
else :
  maxDate = time.strptime("2002-12-31", "%Y-%m-%d")
maxDateStr = '-'.join([str(maxDate.tm_year),str(maxDate.tm_mon),str(maxDate.tm_mday)]) 


#input is the output dataframe of the script model.py 
fin = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/dbEffects2002-12-31.txt'
df = pandas.read_csv(fin,sep="\t",encoding="utf8")

nbMovies = len(pandas.Series(df["movieID"].values.ravel()).unique())
UCnt = df.groupby('userID').agg(['count'])["rating"] #how many movies each user
UCnt = UCnt.ix[:,0]



#####Covariance Matrix : not finished
weight = 1.0/UCnt #vector containing one weight for each user

#intialize matrices
Cov = numpy.asmatrix( numpy.zeros((nbMovies, nbMovies))) 
Wgt = Cov

#generate noise matrix
NoiseCov = numpy.asmatrix( numpy.zeros((nbMovies, nbMovies)))  #noise matrix
NoiseWgt = NoiseCov

#creer dataframe de tous les films
#dans boucle, on va joindre rbarserie à ce df sur les films en left join > Null à r
moviesall = df.groupby('movieID')[['movieID']].max()


#vector rbar for each user = centeredreco for each movie, for 
for user in pandas.Series(df["userID"].values.ravel()).unique():
    rbarSerie = df[["movieID", "centeredRating"]][df["userID"] == user] #je prends films id et rating centered pour mon user
    rbarSerie = pandas.merge(moviesall,rbarSerie, left_on='movieID', right_on='movieID', how='left') #left join on list of unique movies
    rbarSerie = rbarSerie["centeredRating"].fillna(0) #replace NaN from the left join by zeros and keep only centeredRating : this is now a Serie of size nbMovies
    rbarSerie = numpy.asmatrix(rbarSerie.as_matrix()) #convert to an array then a matrix to get the transpose(not working for a 1 dimension vector with array format)
    eu = numpy.where(rbarSerie>0, 1, 0) #should be an array
    eu = numpy.asmatrix(eu)
    rbarMatrix = weight[user] * rbarSerie.T * rbarSerie # matrix size nbMovies^2
    euMatrix = weight[user] * eu.T * eu #idem
    Cov = Cov + rbarMatrix #let's sum baby
    Wgt = Wgt + euMatrix
Cov = Cov + NoiseCov
Wgt = Wgt + NoiseWgt

path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
foutCov = path+'CovMatrix'+maxDate+'.txt'
foutWgt = path+'WgtMatrix'+maxDate+'.txt'

numpy.savetxt(foutCov,Cov,delimiter=',')
numpy.savetxt(foutWgt,Wgt,delimiter=',')

###########################
# NB benjamin : j'ai lancé, ca avait l'air de tourner mais pas encore (26/12) vérifié que les matrice en sortie était juste!
