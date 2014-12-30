##################################################
#Count the unique user,movies,reviews in the directory, for example directories
#computed by prep0 or prep1
##################################################
import os
path = '../testing_2001-01-31'
i = 0
'-'.join(['a', 'b', 'c'])
nReviews = 0
nMovies = 0
setReviewers = set()
for filename in os.listdir(path+'/') :
	fin = open('/'.join([path,filename]),'r')
	fin.readline()
	for line in fin :
		nReviews += 1
		setReviewers.add(line.split(',')[0])
	nMovies += 1
	fin.close()
print("There are %d movies and %d reviews made by %d users" % (nMovies,nReviews,len(setReviewers)))
