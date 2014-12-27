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
listMovies = df.groupby('movieID')['movieID'].max().tolist()
ftest = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/probe.txt'
testset = open(ftest,'r')
testset.readline()
testingSet = []
for line in testset:
    if ':' not in line:
        testingSet.append(int(line.replace('\n','')))


### kNN algorithm from covariance matrix

def getNeighbors(movietest, k): #k nearest neighbors
    similarities = [] #list of tuples with (movies,similarity with movie) 
    for movie2 in listMovies:
        if (movie2 != movietest and movietest in listMovies):
            similarities.append((movie2, Cov[listMovies.index(movietest),listMovies.index(movie2)]))
    similarities.sort(key=operator.itemgetter(1), reverse=True)
    neighbors = []
    for x in range(k):
        neighbors.append(similarities[x][0])
    return neighbors #list of k movieID

def getRating(neighbors): #we have a list of similar movies, now we have to derive the rating
    #option 1 : majority vote
    classVotes = {}
    for x in range(len(neighbors)):
        rating = neighbors[x][1]
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
        if movie in listMovies:
            neighbors = getNeighbors(movie, k)
            result = getRating(neighbors)
        else:
            result = 'NA'
        predictions.append(result)
    accuracymeasures(predictions,testingSet)
    
print kNN(1)
