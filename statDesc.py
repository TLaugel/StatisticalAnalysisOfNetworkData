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
g.vs["type"] = [int(name)%2 == 1 for name in g.vs["name"]]

gmovie =  g.bipartite_projection(types='type',which = 1)
#~ gcust=  g.bipartite_projection(types='type',which = 0)
#~ summary = igraph.summary(g,print_graph_attributes=True, print_vertex_attributes=True, print_edge_attributes=True)
#~ print summary

#~ igraph.summary(gcust)
igraph.summary(gmovie)
timestart =  time.time()
print "diameter of the movie graph : %f" %gmovie.diameter()
print "time to compute diameter %f sec" % int(time.time() - timestart)
#~ timestart =  time.time()
#~ print "clique number of the graph : %f " %gmovie.omega()
#~ print "time to compute clique %d sec" % int(time.time() - timestart)
timestart =  time.time()
a = gmovie.degree_distribution()
print a
print "time to compute degree distribution %d sec" % int(time.time() - timestart)

timestart =  time.time()
gmovie.get_adjacency()
print "time to compute adjacency matrix %d sec" % int(time.time() - timestart)

timestart =  time.time()
print "independence number of the movie graph : %f " %gmovie.alpha()
print "time to compute independence number %d sec" % int(time.time() - timestart)


















