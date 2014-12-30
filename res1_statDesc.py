##########################
#Compute some properties of our graphs
#based mainly on the i-graphs package
##########################
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

if len(list(sys.argv)) > 1 :
  maxDateStr = sys.argv[1]
else :
  maxDateStr = "2000-12-31"

###Create database
path = 'C:/Users/Thibault/Desktop/ENSAE/Cours3A/Network Data/download/'
if sys.platform == 'linux2':
	path = '../'
if not os.path.exists(path+"IgraphEdges") : #igraphe require a specific input format
	fin = open(path+'database_'+maxDateStr+'.txt.gz')
	df = pandas.read_csv(fin,sep=",",encoding="utf8",compression = 'gzip')
	df["userID"] *= 2
	df["movieID"] *= 2
	df["movieID"] += 1
	df[["userID","movieID","rating"]].to_csv(path+"IgraphEdges",sep = "\t",encoding = "utf-8",header = False, index = False)


fin = path+"IgraphEdges"
print "Now let's try Igraph"
g = Graph.Read_Ncol(fin, directed=True,weights = True) #read the graph
g.vs["type"] = [int(name)%2 == 1 for name in g.vs["name"]] #assign the movie or user type : 1 = movie
igraph.summary(g)

timestart =  time.time() ##Not enough RAM, as expected
g.get_adjacency()
print "time to compute the adjacency matrix %d sec" % int(time.time() - timestart)

timestart =  time.time()
a = g.degree_distribution(mode = "in")
print a
print "time to compute inbound (~movies) degree distribution (for the bipartite graph) %d sec" % int(time.time() - timestart)

timestart =  time.time()
a = g.degree_distribution(mode = "out")
print a
print "time to compute outbound (~user) degree distribution (for the bipartite graph) %d sec" % int(time.time() - timestart)

gmovie =  g.bipartite_projection(types='type',which = 1)
guser=  g.bipartite_projection(types='type',which = 0)

summary = igraph.summary(gmovie)

summary = igraph.summary(guser)


igraph.summary(gcust)
igraph.summary(gmovie)
timestart =  time.time()
print "diameter of the movie graph : %f" %gmovie.diameter()
print "time to compute diameter %f sec" % int(time.time() - timestart)

timestart =  time.time()
a = gmovie.degree_distribution()
print a
print "time to compute degree distribution %d sec" % int(time.time() - timestart)

timestart =  time.time()
a = gmovie.degree_distribution()
print a
print "time to compute degree distribution %d sec" % int(time.time() - timestart)

#~ timestart =  time.time() ##too much time to compute
#~ print "clique number of the graph : %f " %gmovie.omega()
#~ print "time to compute clique %d sec" % int(time.time() - timestart)

#~ timestart =  time.time() ##just for testing
#~ gmovie.get_adjacency()
#~ print "time to compute adjacency matrix %d sec" % int(time.time() - timestart) #about 1 second !

#~ timestart =  time.time() ##too much time to compute
#~ print "independence number of the movie graph : %f " %gmovie.alpha()
#~ print "time to compute independence number %d sec" % int(time.time() - timestart)


















