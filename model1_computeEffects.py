import os
import time
import sys
import gzip
import sys
from time import gmtime, strftime
print("starting at "+strftime("%Y %m %d %H:%M:%S", gmtime()))

#maxdate of the previous file
if len(list(sys.argv)) > 1 :
  maxDateStr = sys.argv[1]
else :
  maxDateStr = "2000-12-31"
  
#~ maxDateStr = '-'.join([str(maxDate.tm_year),str(maxDate.tm_mon),str(maxDate.tm_mday)]) 
import pandas, numpy

###Create database
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'
fin = path+'database_'+maxDateStr+'.txt.gz' #csv output file of last python script
#~ fin = path+'test'+'.txt.gz' #csv output file of last python script

df = pandas.read_csv(fin,sep=",",encoding="utf8",compression = 'gzip')
df['num'] = 1
#print(df.shape)
nbMovies = len(pandas.Series(df["movieID"].values.ravel()).unique())
nbUsers = len(pandas.Series(df["userID"].values.ravel()).unique())
print "In the %d reviews, there are %d movies and %d users before %s"% (df.shape[0],nbMovies, nbUsers,maxDateStr)



#############################
#     Recommender engine    #
#############################


#####Global effects
noise = 0 #Generate Noise

GSum = sum(df["rating"]) + noise
GCnt = df.shape[0] + noise
G = GSum/GCnt

#####Movie effects
sigma = .1
noisemovies = [0]*nbMovies #Generate vectors of noise for each movie
noisemovies = numpy.random.normal(0,sigma,nbMovies) #Generate vectors of noise for each movie
betam = 15 #number of fictitious ratings to introduce in the movie average calculation

#####User effects    
betap = 20 #number of fictitious ratings to introduce in the user average calculation
B = 1.0 #bound of the interval that clam the resulted centered rating, to limit sensitivity 
# (???)


MSum = df.groupby('movieID').sum()["rating"] + noisemovies
MCnt = df.groupby('movieID').agg(['count'])["rating"] #agg() creates a dataframe instead of a Series like sum() > impossible to add vector noisemovies
MCnt = MCnt.ix[:,0] + noisemovies
Mavg = (MSum + betam*G)/(MCnt + betam)

Mavg = pandas.DataFrame(Mavg , columns = ['AvgMovie'] )
Mavg.reset_index(inplace = True)
Mavg.set_index(['movieID'])
del MCnt,MSum


UCnt = df.groupby('userID').agg(['count'])["rating"] #how many movies each user
UCnt = UCnt.ix[:,0]

print 'here we go '+strftime("%Y %m %d %H:%M:%S", gmtime())	
df = pandas.merge(df,Mavg,left_on='movieID', right_on='movieID', how='left')
df['ratingCorrected'] = df["rating"] - df['AvgMovie']

r = df.groupby('userID').sum()[["ratingCorrected","num"]]
r['rbar'] = (r['ratingCorrected']+betap*G)/(r["num"] + betap)
r.drop(['num','ratingCorrected'], axis=1, inplace=True)

print 'le plus dur est fait now '+strftime("%Y %m %d %H:%M:%S", gmtime())
#rhat definition
df = pandas.merge(df, r, left_on='userID', right_on=r.index, how='left') 
df.drop(['num','AvgMovie'], axis=1, inplace=True)

df['centeredRating'] = df['ratingCorrected'] - df['rbar']
df.loc[df['centeredRating'] > B ,'centeredRating'] = B
df.loc[df['centeredRating'] < -B ,'centeredRating'] = -B
df.set_index(['userID','movieID'])

###Export database with rhat : 
print "Export the data "+strftime("%Y %m %d %H:%M:%S", gmtime())
fout = path+'dbEffects'+maxDateStr+'.txt'
df.to_csv(fout, sep='\t', encoding='utf-8')
print "Ended at "+strftime("%Y %m %d %H:%M:%S", gmtime())

#######TODO : 
#	add generic path for output file : done
#	better way to do these calculations instead of these dirty loops : done


#export mtnt car prend du temps a computer (etw. 9min)
