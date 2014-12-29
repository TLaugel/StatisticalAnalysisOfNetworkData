import os
import time
import sys
import gzip
#maxdate of the previous file
if len(list(sys.argv)) > 1 :
  maxDateStr = sys.argv[1]
else :
  maxDateStr = "2001-03-31"
  
#~ maxDateStr = '-'.join([str(maxDate.tm_year),str(maxDate.tm_mon),str(maxDate.tm_mday)]) 
#~ print maxDateStr
#to adapt
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download' #file where will be the output .txt : must be in a different file than the input .txt that we created with first python script
#nameDir = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/subtraining_'+'-'.join([str(maxDate.tm_year),str(maxDate.tm_mon),str(maxDate.tm_mday)])  #file where the .txt files that we created with first script are

if sys.platform == 'linux2':
	path = '..'

nameDir = path+'/subtraining_'+maxDateStr
nameDir = path+'/testing_'+maxDateStr
	
if __name__ == "__main__" :
    fout = gzip.open(path+'/database_'+maxDateStr+'.txt.gz','w')
    fout.write('movieID,userID,rating,date\n') 
    for filename in os.listdir(nameDir+'/') :
        movieID = str(int(filename.split('_')[-1].replace('.txt', '')))
        fin = open('/'.join([nameDir,filename]), 'r')
        fin.readline()#on ouvre tout et on lit chaque ligne
        for line in fin :
            res = ""
            res += movieID+','
            res += line
            if res != "":
              fout.write(res)
        fin.close()
    fout.close()




