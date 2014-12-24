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
import pandas, numpy

###Create database
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'
fin = path+'database_'+maxDateStr+'.txt.gz' #csv output file of last python script

df = pandas.read_csv(fin,sep=",",encoding="utf8",compression = 'gzip')
#print(df.shape)
nbMovies = len(pandas.Series(df["movieID"].values.ravel()).unique())
nbUsers = len(pandas.Series(df["userID"].values.ravel()).unique())
print nbMovies, nbUsers



### Recommender engine: following the Microsoft paper

#Global effects
noise = 0 #Generate Noise
GSum = sum(df["rating"]) + noise
GCnt = df.shape[0] + noise
G = GSum/GCnt
#print GSum, GCnt, G

#Movie effects
noisemovies = [0]*nbMovies #Generate vectors of noise for each movie
MSum = df.groupby('movieID').sum()["rating"] + noisemovies
MCnt = df.groupby('movieID').agg(['count'])["rating"] #agg() creates a dataframe instead of a Series like sum() > impossible to add vector noisemovies
MCnt = MCnt.ix[:,0] + noisemovies
betam = 0 #number of fictitious ratings to introduce in the movie average calculation
Mavg = (MSum + betam*G)/(MCnt + betam)

#User effects    
betap = 0 #number of fictitious ratings to introduce in the user average calculation
for user in pandas.Series(df["userID"].values.ravel()).unique():
    moviesSerie = df["movieID"][df["userID"] == user]
    ratingsSerie = df["rating"][df["userID"] == user]
    MavgUser = []#pandas.Series([])
    for movie in moviesSerie:
        MavgUser.append(Mavg[movie])
    ratingsSerie = ratingsSerie.tolist()
    centeredRating = sum([x - y for x, y in zip(ratingsSerie, MavgUser)])
    break

UCnt = df.groupby('userID').agg(['count'])["rating"] 
UCnt = UCnt.ix[:,0]
