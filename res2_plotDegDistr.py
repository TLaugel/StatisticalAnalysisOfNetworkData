################################
#Deprected : originally it was to plot fancy figures
################################
import numpy as np
import matplotlib.pyplot as plt

path = "./"
fin = open(path+'degDistr'+'Movie'+'.txt','r')
for i in range (3):
	fin.readline()
i = 0
d = []
for line in fin :
	try :
		d.append(int(line.split('(')[-1].replace(')\n','')))
	except :
		pass
fin.close()

#we can't see much, and as it is not the aim of our project,
#we did'nt continue in this way
p1 = plt.bar(range(len(d)-1), d[1:], color='r')
plt.show()

