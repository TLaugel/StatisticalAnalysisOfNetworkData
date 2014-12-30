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

#mouais on voit pas grand chose...
#c'est pour ça que j'ai arrete la...
#~ width = 0.35 
p1 = plt.bar(range(len(d)-1), d[1:], color='r')
plt.show()

