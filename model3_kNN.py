##################################################
# kNN algorithm starting from a covariance matrix
#################################################

# NB : still not running properly
# NB2 : now : if a movie from the test dataset is not in the train dataset, 'NA' value is given

import numpy, pandas
import os
import time
import sys
import gzip
import sys
import operator 

#maxdate of the previous file
if len(list(sys.argv)) > 1 :
  maxDate = time.strptime(sys.argv[1],"%Y-%m-%d")
else :
  maxDate = time.strptime("2002-12-31", "%Y-%m-%d")
maxDateStr = '-'.join([str(maxDate.tm_year),str(maxDate.tm_mon),str(maxDate.tm_mday)]) 

maxDate = "2001-12-31"


###Input files : covariance matrix, list of movies, test data
Covin = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/CovMatrix2001-12-31.txt'
Cov = numpy.loadtxt(Covin, delimiter = ',')
fin = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/dbEffects2002-12-31.txt'
df = pandas.read_csv(fin,sep="\t",encoding="utf8")
ftest = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/probe.txt'
testset = open(ftest,'r')
testset.readline()
testingSet = {}
for line in testset:
    if ':' in line:
        movie = int(line.split(':')[0])
        testingSet[movie] = []
    else:
        user = int(line.replace('\n',''))
        testingSet[movie].append(user)
#dic :{movie1:[user1,user2..]}        


listMovies = df.groupby('movieID')['movieID'].max().tolist()
listUsers = df.groupby('userID')['userID'].max().tolist()



### kNN algorithm from covariance matrix

def getNeighbors(moviesviewed, movietest, k): #k nearest neighbors among the movies that the user has already seen
    similarities = [] #list of tuples with (movies,similarity with movie)
    for movie2 in moviesviewed: #moviestrain is the list of movieIDs that the current user has viewed
        if (movie2 != movietest and movietest in listMovies): #listmovies is the list of movies in the covariance matrix: has to be in it
            similarities.append((movie2, Cov[listMovies.index(movietest),listMovies.index(movie2)]))
    similarities.sort(key=operator.itemgetter(1), reverse=True)
    neighbors = []
    for x in range(k):
        neighbors.append(similarities[x][0])
    return neighbors

def getRating(userviewed, neighbors): #we have a list of similar movies, now we have to derive the rating
    #option 1 : majority vote
    classVotes = {}
    for x in range(len(neighbors)):
        neighbor = neighbors[x] #scalar, it is the movieID of the neighbor
         #on a une liste de films proches, mais quel rating attribue-t-on à ce film?
                #1. majorité/moyenne des ratings (bad but ez)
                #2. 
        rating = float(userviewed.ix[:,1][userviewed.ix[:,0]==neighbor]) #scalar
        if rating in classVotes:
            classeVotes[rating] +=1
        else:
            classVotes[rating] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def accuracymeasures(predictions, targets): #compute RMSE and % of well-predicted data
    idx_remove = []
    predictions2 = []
    targets2 = []
    for x in range(len(predictions)):
        if predictions[x]=='NA':
            idx_remove.append(x)
    for x in range(len(predictions)):
        if x not in idx_remove:
            predictions2.append(predictions[x])
            targets2.append(targets[x])
            
    wellPred = 0
    for k in range(len(predictions2)):
        if predictions2[k] == targets2[k]:
            wellPred +=1
    acc = wellPred/len(targets2)
    rmse = numpy.sqrt(((predictions2 - targets2) ** 2).mean())
    print 'RMSE = '+str(rmse)
    print 'Accuracy = '+str(100*acc)+'%'


def kNN(k):
    predictions = []
    for movie in testingSet:
        userlist = testingSet[movie]
        for user in userlist:
            if user in listUsers:
                userviewed = df[df['userID']==user][['movieID','rating']]
                moviesviewed = userviewed['movieID'].tolist()
            else :
                userviewed = df.groupby('movieID')[['movieID', 'rating']].agg(['mean'])
                userviewed = numpy.round(userviewed) #we want integer values
                moviesviewed = userviewed['movieID']['mean'].tolist()
                break
            if movie in listMovies: #movie we want to get the neighbors of has to be in the cov matrix
                neighbors = getNeighbors(moviesviewed, movie, k) #list of closest movies he has viewed
                result = getRating(userviewed, neighbors)  #rating value
            else:
                result = 'NA'
            predictions.append(result)
            break
        
    accuracymeasures(predictions,testingSet)
    
print kNN(1)


################
# TODO : testing set à enlever du train
# what if k>number of movies viewed (compléter avec des génériques..)
