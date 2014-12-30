####################################
#Create the row CSV from the output of prep0, and prep1
####################################
import os
import time
import sys
import gzip

if len(list(sys.argv)) > 1 :
  maxDateStr = sys.argv[1]
else :
  maxDateStr = "2001-01-31"
  

path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download' #file where will be the output .txt : must be in a different file than the input .txt that we created with first python script
if sys.platform == 'linux2':
	path = '..'

nameDir = path+'/subtraining_'+maxDateStr
nameDir = path+'/testing_'+maxDateStr
	
if __name__ == "__main__" :
    fout = gzip.open(path+'/database_'+maxDateStr+'.txt.gz','w')
    fout.write('movieID,userID,rating,date\n') 
    for filename in os.listdir(nameDir+'/') : #for every file in the directory (created by the scripts prep0 or prep1)
        movieID = str(int(filename.split('_')[-1].replace('.txt', '')))
        fin = open('/'.join([nameDir,filename]), 'r')
        fin.readline() #skipping the header
        for line in fin : #adding all the contents in the csv
            res = ""
            res += movieID+','
            res += line
            if res != "":
              fout.write(res)
        fin.close()
    fout.close()




