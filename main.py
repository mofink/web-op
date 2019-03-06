#main.py

from genetics import *

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
#warnings.filterwarnings("ignore", category=RuntimeWarning) 

def main():
	#Genetics(filename,number of detectors,number of features (dimensions of data), radius,alpha,beta, population size, prob of mutation, prob of crossover, number of gen)
	a = Genetics('iris.csv',100,2,0.1,1,0.5,0.1,0.9,100)
	fitness_array = []
	for gen_num in range(a.total_gen):
		a.pop = a.new_gen(a.pop,gen_num)
		fitness_array.append((a.findFitness(a.pop))) #save avg fitness of each generation
		if gen_num%10==0:
			print '%d%%' %(gen_num)


	a.final_pop = a.pop
	x = []
	y = []
	for i in range(len(fitness_array)):
		x.append(i)
		y.append(fitness_array[i])
	
	
	plt.plot(x,y)
	plt.show()

	


main()
