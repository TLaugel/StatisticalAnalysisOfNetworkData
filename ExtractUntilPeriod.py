import os
import time
import sys
liDates = []
if len(list(sys.argv)) > 1 :
	liDates = sys.argv[1:]
	liDatesLi = [ el.split('-') for el in liDates]
else :
	liDates = ["2002-12-31"]
	
start_path = ''
if sys.platform == 'linux2':
	start_path = '../'
	
i = 0
nReviews = 0
nMovies = 0
setReviewers = set()

path = start_path + 'training_set/'
nameDir = {}
for maxDate in liDates :
	nameDir[maxDate] = start_path+ 'subtraining_' + maxDate
	if not(os.path.exists(nameDir[maxDate] )):
		os.mkdir(nameDir[maxDate] )

def isDateGreater_aux(li1,li2) :
	if li1 == [] :
		return False
	if li1[0] > li2[0] :
		return True
	if li1[0] < li2[0] :
		return False
	return isDateGreater_aux(li1[:-1],li2[:-1])
	
#~ def isDateGreater(str1,str2):
	#~ li1 = str1.split('-')
	#~ li2 = str2.split('-')
	#~ li1 = map(int,li1)
	#~ li2 = map(int,li2)
	#~ return isDateGreater_aux(li1,li2)
		
if __name__ == "__main__" :
	for filename in os.listdir(path) :
		fin = open('/'.join([path,filename]),'r')
		fin.readline()
		resDic = {}
		for maxDate in liDates :
			resDic[maxDate] = ""
			
		for line in fin :
			nReviews += 1
			parsed = line.split(',')
			setReviewers.add(parsed[0])
			currDateStr = parsed[-1].replace('\r','').replace('\n','')
			liRevDate = currDateStr.split('-')
			for maxDateLi in liDatesLi :
				if isDateGreater_aux(maxDateLi,liRevDate):
					resDic['-'.join(maxDateLi)] += line
		nMovies += 1
		for maxDate in resDic :
			res = resDic[maxDate]
			if res != "" :
				fout = open(nameDir[maxDate]+'/'+filename,'w')
				fout.write(res)
				fout.close()
		fin.close()
	