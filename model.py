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



#############################
#     Recommender engine    #
#############################


#####Global effects
noise = 0 #Generate Noise

GSum = sum(df["rating"]) + noise
GCnt = df.shape[0] + noise
G = GSum/GCnt



#####Movie effects
noisemovies = [0]*nbMovies #Generate vectors of noise for each movie
betam = 0 #number of fictitious ratings to introduce in the movie average calculation

MSum = df.groupby('movieID').sum()["rating"] + noisemovies
MCnt = df.groupby('movieID').agg(['count'])["rating"] #agg() creates a dataframe instead of a Series like sum() > impossible to add vector noisemovies
MCnt = MCnt.ix[:,0] + noisemovies
Mavg = (MSum + betam*G)/(MCnt + betam)



#####User effects    
betap = 0 #number of fictitious ratings to introduce in the user average calculation
B = 0 #bound of the interval that clam the resulted centered rating, to limit sensitivity 
# (???)

UCnt = df.groupby('userID').agg(['count'])["rating"] #how many movies each user
UCnt = UCnt.ix[:,0]
r = {}
print 'here we go'
for user in pandas.Series(df["userID"].values.ravel()).unique():
    moviesSerie = df["movieID"][df["userID"] == user]
    ratingsSerie = df["rating"][df["userID"] == user]
    MavgUser = []#pandas.Series([])
    for movie in moviesSerie:
        MavgUser.append(Mavg[movie])
    ratingsSerie = ratingsSerie.tolist()
    centeredRating = sum([x - y for x, y in zip(ratingsSerie, MavgUser)])
    r[user] = (centeredRating + betap*G)/(UCnt[user] + betap)
print 'le plus dur est fait now'
r = pandas.DataFrame(r.items(), columns=['userID', 'rbar'])

#rhat definition
df = pandas.merge(df, r, left_on='userID', right_on='userID', how='left') 
df['centeredRating'] = min(max(df['rating'] - df['rbar'],-1*B),B) #(centered rating or rhat)
# last line does not work : problem with taking the min of a serie



###### Ici, sortir un csv avec nouveau dataframe ou trouver moyen plus propre d'écrire la boucle sale (prend du temps (autour de 5min))


"""
#####Covariance Matrix : not finished
weight = 1/sum(UCnt) #vector containing one weight for each user

#intialize matrices
Cov = numpy.zeros((nbMovies, nbMovies)) 
Wgt = Cov

#generate noise matrix
NoiseCov = numpy.zeros((nbMovies, nbMovies))  #noise matrix
NoiseWgt = NoiseCov

#vector rbar for each user = centeredreco for each movie, for 
for user in pandas.Series(df["userID"].values.ravel()).unique():
    rbarSerie = df["centeredRating"][df["userID"] == user]
    rbarSerie = rbarSerie.tolist() #tf en matrix pr multiplica matricielle?
    #rbarMatrix = weight[user] * rbar * transpose(rbar) > matrix size d*d

    #computer vecteur de 1 et 0 si un utilisateur a recommendé un film:
        moviesSerie = df["movieID"][df["userID"] == user] #serie des films que l'user a regardé
        #creer liste de 0 de taille nbMovies, et remplacer par moviesSerie les valeurs avec les index correspondants
        #puis 1 si >0, 0 sinon. = vecteur binaire de Moviesvec
    #euMatrix = weight[user] * Moviesvec * transpose(Moviesvec) > matrixe size d*d
    
    Cov = Cov + rbarMatrix
    Wgt = Wgt + euMatrix
Cov = Cov + NoiseCov
Wgt = Wgt + NoiseWgt

#ici on va extraire les matrices (deux fichiers txt, ou un seul séparé par un truc)


##################################
#Fonctions à creer
##################################
# eu =vecteur binaire pour chaque user, chaque coordonnée étant un film. 1 si le user a review le film, 0 sinon
"""
