import os
import time
import sys
if len(list(sys.argv)) > 1 :
	#~ print str(sys.argv)[1]
	maxDate = time.strptime(sys.argv[1],"%Y-%m-%d")
else :
	maxDate = time.strptime("2002-12-31", "%Y-%m-%d")
path = '../training_set/'
i = 0
nReviews = 0
nMovies = 0
setReviewers = set()
nameDir = '../subtraining_'+'-'.join([str(maxDate.tm_year),str(maxDate.tm_mon),str(maxDate.tm_mday)])
maxDateStr = nameDir.split('_')[-1]
if not(os.path.exists(nameDir)):
	os.mkdir(nameDir)
def isDateGreater_aux(li1,li2) :
	if li1 == [] :
		return False
	if li1[0] > li2[0] :
		return True
	if li1[0] < li2[0] :
		return False
	return isDateGreater_aux(li1[:-1],li2[:-1])
def isDateGreater(str1,str2):
	li1 = str1.split('-')
	li2 = str2.split('-')
	li1 = map(int,li1)
	li2 = map(int,li2)
	return isDateGreater_aux(li1,li2)
		
if __name__ == "__main__" :
	for filename in os.listdir(path+'/') :
		fin = open('/'.join([path,filename]),'r')
		fin.readline()
		if not os.path.isdir('../nameDir') :
			os.mkdir('../nameDir')
		res = ""
		for line in fin :
			nReviews += 1
			parsed = line.split(',')
			setReviewers.add(parsed[0])
			currDateStr = parsed[-1].replace('\r','').replace('\n','')
			if isDateGreater(maxDateStr,currDateStr):
				res += line
		nMovies += 1
		if res != "":
			fout = open(nameDir+'/'+filename,'w')
			fout.write(res)
			fout.close()
		fin.close()
	