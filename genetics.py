import numpy as np
import random
from sklearn import preprocessing
from sklearn.neighbors import KDTree
import math
from pprint import pprint
import matplotlib.pyplot as plt


class Genetics(object):

	def __init__(self,fn,pop_count,num_of_features,rs,alpha,beta,prob_of_m,prob_of_cross,total_gen):
		self.pop_count = pop_count
		self.num_of_features = num_of_features
		self.rs = rs
		self.alpha = alpha
		self.beta = beta
		self.prob_of_m = prob_of_m
		self.prob_of_cross = prob_of_cross
		self.total_gen = total_gen
		self.self_pop = self.selfPopulation(fn)
		self.new_pop = self.createPopulation()

	def selfPopulation(self,fn):
		#note that self in the class is not the same as "self" in the problem statement

		self.data = np.genfromtxt(fn,delimiter=',') #read csv
		self.data = self.data[:50]#remove non-setosa
		self.data = self.data[~np.isnan(self.data)] #remove meta data
		
		self.grouped_data = [] #group into chromosomes
		i = 0
		while i < len(self.data):
			self.grouped_data.append(self.data[i:i+4]) #this needs to be changed for different data sets - fix this?
			i+=4

		for ch in range(len(self.grouped_data)):
			self.grouped_data[ch] = self.grouped_data[ch][:self.num_of_features] #reduce to 2D problem

		#self_data is the normalized self population grouped into chromosomes with two elements each
		self.self_data = preprocessing.normalize(self.grouped_data)
		return self.self_data

	def createPopulation(self):
		self.pop = []
		for ch in range(self.pop_count):
			self.pop.append([random.random() for i in range(self.num_of_features)]) #one chromosome

		return self.pop

	def findFitness(self,pop):
		#http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html
		
		if(sum(1 for x in pop if isinstance(x,list))) > 1:
			#D1
			tree = KDTree(pop,leaf_size=30,metric='euclidean')
			D1 = [] #distance to nearest neighbor in pop itself
			for ch in range(len(pop)):
				X = pop[ch]
				dist,ind = tree.query(X,k=2,return_distance=True)
				D1.append(dist[0][1]) #now we have a list of the distance of each chromosome to closest neighbor in same population
				
			#D
			tree = KDTree(self.self_pop,leaf_size=30,metric='euclidean')
			D = []
			for ch in range(len(pop)):
				X = pop[ch]
				dist,ind = tree.query(X,k=2,return_distance=True)
				D.append(dist[0][1]) #now we have a list of the distance of each chromosome to closest neighbor in self population

			alpha_term = beta_term = []
			for bbb,ccc in zip(D,D1):
				if(bbb!=0 and ccc!=0):
					alpha_term.append(self.alpha*math.exp(-self.rs/bbb))
					beta_term.append(self.beta*math.exp(-self.rs/ccc))
				elif(bbb==0 and ccc==0):
					alpha_term.append(0)
					beta_term.append(0)
				elif(bbb==0 and ccc!=0):
					alpha_term.append(0)
					beta_term.append(self.beta*math.exp(-self.rs/ccc))
				else:
					alpha_term.append(self.alpha*math.exp(-self.rs/bbb))
					beta_term.append(0)

			fitness_list = []
			for i in range(len(alpha_term)):
				fitness_list.append(alpha_term[i] + beta_term[i]) 

			fitness = np.mean(fitness_list)
			return fitness

		else: #fitness of single chromosome, beta term is 0. Some of this code is unneeded, cleanup later
			#D
			tree = KDTree(self.self_pop,leaf_size=30,metric='euclidean')
			D = []
			X = pop
			dist,ind = tree.query(X,k=2,return_distance=True)
			D.append(dist[0][1]) 


			alpha_term = beta_term = []
			for bbb in D:
				if bbb!=0:
					alpha_term.append(self.alpha*math.exp(-self.rs/bbb))
				else:
					alpha_term.append(0)
			
			fitness_list = []
			for i in range(len(alpha_term)):
				fitness_list.append(alpha_term[i]) 

			fitness = np.mean(fitness_list)
			return fitness

	def new_gen(self,pop,gen_num): #keep track of what generation we are in for mutation function
		next_pop = []
		for aaa in range(len(pop)/2):
			cross = []
			#we need a set of two chromosomes, add each set to cross[]
			for i in range(2):
				#pick a set of 2 random chromosomes
				num = random.randint(0,len(pop)-1)
				ch1 = pop[num]
				num = random.randint(0,len(pop)-1)
				ch2 = pop[num]
				if(self.findFitness(ch1) > self.findFitness(ch2)):
					cross.append(ch1)
				else:
					cross.append(ch2)


			#probablity of cross over
			num = random.random()
			if num < self.prob_of_cross: #crossover		
				new_ch1 = [cross[0][0],cross[1][1]]
				new_ch2 = [cross[1][0],cross[0][1]]
			else: #don't cross
				new_ch1 = [cross[0][0],cross[0][1]]
				new_ch2 = [cross[1][0],cross[1][1]]

			#add floating point mutation
			#http://umsl.edu/divisions/artscience/math_cs/about/People/Faculty/CezaryJanikow/folder%20two/Experimental.pdf
			num = random.random() #crossover and mutation are independent
			if num > self.prob_of_m:
				new_ch1 = self.mutate(new_ch1,gen_num)
			else:
				pass

			#pass new genes into new population
			next_pop.append(new_ch1)
			next_pop.append(new_ch2)
		
		#pass on population with higher fitness
		if(self.findFitness(pop) > self.findFitness(next_pop)):
			return pop
		else:
			return next_pop

	def mutate(self,ch,gen_num): #mutate a gene
		num = random.random()
		m_num = random.random() #probability of which gene to mutate:
		if m_num > 0.5:
			m_gene = 0
		else:
			m_gene = 1
		if num > 0.5: #add
			m_function = (1-ch[m_gene])*(1-random.random()**(1-gen_num/self.total_gen)**5)
			ch[m_gene] = ch[m_gene] + m_function
		else: #subtract
			m_function = ch[m_gene]*(1-random.random()**(1-gen_num/self.total_gen)**5)
			ch[m_gene] = ch[m_gene] - m_function

		return ch

	#def plotFitness(self,pop): #defunct. Ignore for now
		x = y = []

		for gene in range(len(pop)):
			x.append(gene)
			y.append(pop[gene])

		plt.scatter(x,y)
		plt.show()

		

