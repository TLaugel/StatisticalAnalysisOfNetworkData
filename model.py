import pandas, numpy

###Create database
fin = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/database2002-12-31.txt' #csv output file of last python script
df = pandas.read_csv(fin,sep=",",encoding="utf8")
#print(df.shape)
nbMovies = len(pandas.Series(df["movieID"].values.ravel()).unique())
nbUsers = len(pandas.Series(df["userID"].values.ravel()).unique())
#print nbMovies, nbUsers



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
