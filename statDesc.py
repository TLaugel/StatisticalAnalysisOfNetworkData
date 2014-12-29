import os
import time
import sys
import gzip
import sys
from time import gmtime, strftime
import igraph
from igraph import Graph
import pandas
print("starting at "+strftime("%Y %m %d %H:%M:%S", gmtime()))

#maxdate of the previous file
if len(list(sys.argv)) > 1 :
  maxDateStr = sys.argv[1]
else :
  maxDateStr = "2000-12-31"
  
#~ maxDateStr = '-'.join([str(maxDate.tm_year),str(maxDate.tm_mon),str(maxDate.tm_mday)]) 
#~ import pandas, numpy

###Create database
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'
if not os.path.exists(path+"IgraphEdges") :
	fin = open(path+'database_'+maxDateStr+'.txt.gz') #csv output file of last python script
	#~ fin = open(path+'testIgraph.txt') #csv output file of last python script
	#~ fin.readline()
	df = pandas.read_csv(fin,sep=",",encoding="utf8",compression = 'gzip')
	df["userID"] *= 2
	df["movieID"] *= 2
	df["movieID"] += 1
	df[["userID","movieID","rating"]].to_csv(path+"IgraphEdges",sep = "\t",encoding = "utf-8",header = False, index = False)
#~ df[["rating"]].to_csv(path+"IgraphValue",sep = "\t",encoding = "utf-8")

fin = path+"IgraphEdges"
print "Now let's try Igraph"
g = Graph.Read_Ncol(fin)
#~ print g.vs["name"][1:10]
#~ print g.es["weight"][1:10]
g.vs["type"] = [int(name)%2 == 0 for name in g.vs["name"]]
gcust, gmovie =  g.bipartite_projection(types='type')
igraph.summary(g)

igraph.summary(gcust)
igraph.summary(gmovie)