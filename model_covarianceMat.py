#######################
# model part 2: computation of covariance and weight matrices
#########################

#input is the output dataframe of the script model.py 
fin = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/dbEffects2002-12-31.txt'
df = pandas.read_csv(fin,sep="\t",encoding="utf8")

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
    rbarSerie = rbarSerie["centeredRating"].fillna(0) #replace NaN from the left join by zeros and keep only centeredRating : this is now a vector of size nbMovies
    rbarSerie = numpy.asmatrix(rbarSerie.as_matrix()) #convert to matrix to get the transpose(not working for a 1 dimension vector with array format)
    rbarMatrix = weight[user] * rbarSerie.T * rbarSerie # matrix size nbMovies^2
    Cov = Cov + rbarMatrix #let's sum baby
Cov = Cov + NoiseCov

###########################
# TODO : include (in the loop) calculation of the weight matrix
# NB benjamin : j'ai lancé, ca avait l'air de tourner mais pas encore (25/12) vérifié que la matrice en sortie était juste!
