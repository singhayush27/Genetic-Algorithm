import random
import numpy as np
import time
class geneticAlgorithm:
    def __init__(self,target=[1,2,3,4,5,6,7,8,0],
                            initialPopulation='random',MatingPoolSize=10):
        self.fitnes=[]
        self.target=target
        self.MatingPoolSize=MatingPoolSize
        if initialPopulation=='random':
            print(self.MatingPoolSize)
            self.Population=self.generateInitialPopulation(self.MatingPoolSize)
        else:
            self.Population=initialPopulation
    def fitness(self,matrix):
        return np.count_nonzero(np.array(self.target)==np.array(matrix))*8+1
    def generateInitialPopulation(self,MatingPoolSize):
        population=[]
        print("initial Population selected at random")
        for i in range(MatingPoolSize):population.append(random.sample(range(9),9))        
        for people in population:print(people)
        return population
    def matingPool(self):
        childrens=[]
        for i in range(int(self.MatingPoolSize/2)):
            parents=random.choices(population=self.Population,weights=self.fitnes,k=2)
            child1,child2=parents[0][:5],parents[1][:5]
            mutation1,mutation2=random.randint(0,4),random.randint(5,8)
            child1+=[x for x in parents[1] if x not in child1]
            child2+=[x for x in parents[0] if x not in child2]
            child1[mutation2],child1[mutation1]=child1[mutation1],child1[mutation2]
            child2[mutation2],child2[mutation1]=child2[mutation1],child2[mutation2]
            childrens+=[child1,child2]
        return childrens
    def Start_GA(self):
        start_time=time.time()
        for i in range(10000):
            for parent in self.Population:self.fitnes.append(self.fitness(parent))
            Off_springs=self.matingPool()
            if self.target in Off_springs:
                print("Found target\n","Total runs=",i,'\n',
                    "Final Mating pool\n",'fitness=',self.fitnes)
                for parent in self.Population:print(parent)
                break
            self.fitnes.clear()
            self.Population=Off_springs
        return time.time()-start_time,
GA=geneticAlgorithm()
GA.Start_GA()