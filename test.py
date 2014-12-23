import os
path = 'training_set'
i = 0
'-'.join(['a', 'b', 'c'])
nReviews = 0
nMovies = 0
setReviewers = set()
for filename in os.listdir(path+'/') :
	#~ i += 1
	#~ if i > 100 :
		#~ break
	#~ fout = open('subtraining/'+filename,'w')
	fin = open('/'.join([path,filename]),'r')
	fin.readline()
	for line in fin :
		nReviews += 1
		setReviewers.add(line.split(',')[0])
	nMovies += 1
	#~ fout.write(fin.read())
	fin.close()
	#~ fout.close()
print("il y a %d films et %d reviews pour %d user" % (nMovies,nReviews,len(setReviewers)))