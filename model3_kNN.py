# -*- coding: utf8 -*-
##################################################
# kNN algorithm starting from a covariance matrix
#################################################

# NB : still not running properly
# NB2 : now : if a movie from the test dataset is not in the train dataset, 'NA' value is given


import numpy, pandas
import os
import time
import sys
import zipimport
from sklearn.metrics import confusion_matrix
import operator
import math
from sklearn.metrics import mean_squared_error

#maxdate of the previous file
if len(list(sys.argv)) > 1 :
  maxDate = sys.argv[1]
else :
  maxDate ="2000-12-31"


###Input files : covariance matrix, list of movies, test data
timestart =  time.time()
#~ print timestart

path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'
Covin = path+'CovMatrix_'+maxDate+'.txt'
Cov = numpy.loadtxt(Covin, delimiter = ',')
print 'time to import Cov: '+ str((time.time()-timestart)/60)

fin = path+'dbEffects'+maxDate+'.txt'
df = pandas.read_csv(fin,sep="\t",encoding="utf8")
ftest = path+'database_'+maxDate+'_Test.txt.gz'
#~ ftest = path+'test'
dfTest = pandas.read_csv(ftest,sep=",",encoding="utf8",compression = 'gzip')
print dfTest.shape
#~ dfTest = dfTest.head(100)
#~ dfTest = pandas.read_csv(ftest,sep=",",encoding="utf8")
print 'time to import Cov + Train and Test dataframes: '+ str((time.time()-timestart)/60)

print 'hey ho let s go'
### kNN algorithm from covariance matrix
listMovies = df.groupby('movieID')['movieID'].max().tolist()
DicMovies = {}
index = 0
for el in listMovies :
	DicMovies[el] = index
	index += 1
listUsers = df.groupby('userID')['userID'].max().tolist()
DicUsers = {}
index = 0
for el in listUsers :
	DicUsers[el] = index
	index += 1

def getNeighbors(moviesviewed, movietest, k): #k nearest neighbors among the movies that the user has already seen
    similarities = [] #list of tuples with (movies,similarity with movie)
    i_movieTest = DicMovies[movietest]
    for movie2 in moviesviewed: #moviestrain is the list of movieIDs that the current user has viewed
        if (movie2 != movietest and movietest in DicMovies): #listmovies is the list of movies in the covariance matrix: has to be in it
            similarities.append((movie2, Cov[i_movieTest,DicMovies[movie2]]))
    similarities.sort(key=operator.itemgetter(1), reverse=True)
    
    #~ for x in range(min(k,len(similarities))):
        #~ neighbors.append(similarities[x][0])
    n = min(k,len(similarities))
    neighbors = [el[0] for el in similarities[0:n]]
    #~ neighbors = [0]*n
    #~ for x in range(n):
        #~ neighbors[x] = similarities[x][0]
    return neighbors

def getRating(userviewed, neighbors): #we have a list of similar movies, now we have to derive the rating
    #option 1 : majority vote
    classVotes = {}
    for x in range(len(neighbors)):
        neighbor = neighbors[x] #scalar, it is the movieID of the neighbor
        rating = float(userviewed.ix[:,1][userviewed.ix[:,0]==neighbor]) #scalar
        if rating in classVotes:
            classVotes[rating] += 1
        else:
            classVotes[rating] = 1
    #~ sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    #~ return sortedVotes[0][0]
    return max(classVotes.iteritems(),key=operator.itemgetter(1))[0] #if I understand correctly you don't have to sort, you just take the max

def accuracymeasures(predictions, dataTest):
    #1 remove NA and corresponding lines in dataTest
    idx_remove = []
    predictions2 = []
    targets2 = []
    for x in range(len(predictions)):
        if predictions[x]=='NA':
            idx_remove.append(x)
        else :
            predictions2.append(predictions[x])
            targets2.append(dataTest['rating'].tolist()[x])
    #2 Accuracy measures: RMSE, accuracy percentage and confusion table
    #accuracy
    wellPred = 0
    for k in range(len(predictions2)):
        if predictions2[k] == targets2[k]:
            wellPred +=1
    acc = float(wellPred)/len(targets2)    
    #rmse
    #~ s = numpy.mean((predictions2 - targets2)**2)
    #~ s = 0
    #~ for i in range(len(predictions2)):
        #~ s += (predictions2[i] - targets2[i])**2
    rmse = math.sqrt(mean_squared_error(predictions2,targets2))    
    #ROC
    roc = confusion_matrix(targets2, predictions2)  
    print '______________________________'
    print '           Accuracy'
    print 'RMSE = '+str(rmse)
    print 'Accuracy = '+str(100*acc)+'%'
    print ' '
    print 'Confusion matrix:'
    print roc
    print '______________________________'


def kNN(k):
    predictions = []
    for movie in (dfTest['movieID']).unique():
        userlist = dfTest[dfTest['movieID']==movie]['userID'].tolist()
        #print 'movie  ' + str(movie)
        #print 'userlist : '
        #print userlist
        #print '___'
        for user in userlist:
            if movie not in DicMovies : #movie we want to get the neighbors of has to be in the cov matrix
                predictions.append('NA')
                continue
            if user in DicUsers:
                #print 'user ok'
                userviewed = df[df['userID']==user][['movieID','rating']]
                moviesviewed = userviewed['movieID'].tolist()
            else :
                #print 'we aggregate'
                userviewed = df.groupby('movieID')[['movieID', 'rating']].agg(['mean'])
                userviewed = numpy.round(userviewed) #we want integer values
                moviesviewed = userviewed['movieID']['mean'].tolist()
            neighbors = getNeighbors(moviesviewed, movie, k) #list of closest movies he has viewed
            result = int(getRating(userviewed, neighbors) ) #rating value
            predictions.append(result)
    return accuracymeasures(predictions,dfTest)
    #il faudra printer la table aussi après
    
#k=3  RMSE=1.0 , acc = 27%
print "Oh yeah baby"
kNN(20)

print "Computation time: %f min"%((time.time()-timestart)/60)
