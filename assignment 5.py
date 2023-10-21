#!/usr/bin/env python
# coding: utf-8

# In[78]:


import copy  
import numpy as np
import math
import pandas as pd
import time
import random


# In[79]:


class Node:
    def __init__(self,grid,h_value=0,hv=' '):
        self.grid=grid
        self.h_value=h_value
        self.g_ofn=0
        self.parent=None


# In[80]:


Goal=[[ 1,2,3],[4,5,6],[7,8,' ']]
goal=copy.deepcopy(Goal) 
goal=[*goal[0],*goal[1],*goal[2]] 
goal[goal.index(' ')]=0 
goal=np.array(goal).reshape(3,3)
MatingPoolSize=10 
fitnes=[] 
target=[1,2,3,4,5,6,7,8,0]
initialMatrix=[]


# In[81]:


def check_solvability(temp):
    list_of_inversions=[]
    temp.remove( ' ')
    inversions=0
    for i in temp:
        for j in temp[temp.index(i):]:
            if  j<i:
                inversions+=1 
        list_of_inversions.append(inversions)
        inversions=0
    if(sum(list_of_inversions)%2!=0): 
        print("puzzle not solvable\n") 
        return False
    else:print("puzzle solvable\n")
    return True


# In[82]:


check_solvability([5,' ',8,4,2,1,7,3,6])


# In[83]:


def h(child,string,h_val=0):
    if string== 'Misplaced':
        child=[*child[0],*child[1],*child[2]]
        goal_copy=[*Goal[0],*Goal[1],*Goal[2]]
        for i in range(len(child)):
            if(child[i]!=goal_copy[i]):
                h_val+=1
        return h_val
    if string== 'Manhatten':
        child=[*child[0],*child[1],*child[2]]
        child[child.index(' ')]=0
        child=np.array(child).reshape(3,3)
        for i in child.reshape(1,9)[0]:
            child_loc=np.array(np.where(child==i))
            goal_loc=np.array(np.where(goal==i))
            h_val+=np.sum(np.absolute(child_loc-goal_loc))
        return h_val


# In[84]:


def fitness(matrix,choice):
    sum=1
    if(choice=='MatchedTiles'):
        return np.count_nonzero(np.array(target)==np.array(matrix))*8
    if(choice=='other'):
        for ind,i in enumerate(matrix):sum+=abs(ind-target.index(i))
        return round(1/sum,2)


# In[85]:


def find_children(parent):
    parent_matrix=parent.grid
    if(parent_matrix==Goal):return 'stop'
    for bi,i in enumerate(parent_matrix):
        if ' ' in i:
            bj=i.index(' ') 
            break
    next_coordinates=list(filter(lambda x:not((x[0]>2 or x[0]<0) or (x[1]>2 or x[1]<0)), [[bi-1,bj],[bi+1,bj],[bi,bj-1],[bi,bj+1]]))
    new_matrices=[]
    expanded= False
    for i,j in next_coordinates:
        child=copy.deepcopy(parent_matrix)
        child[bi][bj]=child[i][j]
        child[i][j]=' ' 
        new_matrices.append(child)
    return new_matrices




# In[86]:


def generateinitialPopulation():
    population=[]
    print("initial Population selected at random")
    population.append(initialMatrix)
    for i in range(MatingPoolSize-1):population.append(random.sample(range(9),9))
    for people in population:print(people)
    return population


# In[87]:


def matingPool(mates,fit):
    childrens=[]
    for i in range(int(MatingPoolSize/2)):
        parents=random.choices(population=mates,weights=fit,k=2)
        child1,child2=parents[0][:5],parents[1][:5] 
        mutation1,mutation2=random.randint(0,4),random.randint(5,8) 
        child1+=[x for x in parents[1] if x not in child1] 
        child2+=[x for x in parents[0] if x not in child2]
        child1[mutation2],child1[mutation1]=child1[mutation1],child1[mutation2] 
        child2[mutation2],child2[mutation1]=child2[mutation1],child2[mutation2] 
        childrens+=[child1,child2]
    return childrens


# In[88]:


def solve(heuristic,temp=6):
    if(heuristic=='SA Misplaced' or heuristic=='SA Manhatten'): 
        start_time=time.time()
        no_of_matrices=0
        parent=Node(start,h(start,heuristic[3:])) 
        list1=[]
        parent.g_ofn=0
        while temp>0.03: 
            temp-=0.00005
            children=find_children(parent)
            for index,child in enumerate(children): 
                no_of_matrices+=1 
                node=Node(child,h(child,string=heuristic[3:])) 
                node.parent=parent
                node.g_ofn=node.parent.g_ofn+1 
                if(child==Goal):
                    print('target found')
                    return time.time()-start_time,(6-temp)/0.00005,node.g_ofn,no_of_matrices,'Success' 
                list1.append(node)
            child=random.choice(list1) 
            list1.clear()
            if(parent.h_value-child.h_value>0 or
               math.exp(round((parent.h_value-child.h_value if parent.h_value-child.h_value!=0 else -1)/temp,5))>random.uniform(0,1)):
                parent=child
        return time.time()-start_time,(6-temp)/0.00005,node.g_ofn,no_of_matrices,'Failure'

    # Genetic Algorithm

    else:
        print("**************************************************\n\n") 
        print("Starting Genetic Algorithm") 
        Population=generateinitialPopulation()
        print(heuristic[3:])
        for i in range(10000): 
            start_time=time.time()
            for parent in Population:fitnes.append(fitness(parent,heuristic[3:])) 
            Off_springs=matingPool(Population,fitnes)
            if target in Off_springs:
                print("Found target\n","Total runs=",i,'\n',"Final Mating pool\n","fitness=",fitnes)
                for parent in Population:print(parent)
                fitnes.clear()
                break
            fitnes.clear()
            Population=Off_springs
        return time.time()-start_time,i,None,i*10,'Success'




# In[89]:


def Assignment(): 
    list_of_h=['SA Misplaced','SA Manhatten','GA MatchedTiles', 'GA other']
    rows=['Time taken','Total number of states explored', 'Total number of states on optimal path', 'Total number of matrices expanded','Sucess or failure message'] 
    df=pd.DataFrame(0,index=rows,columns=list_of_h) 
    for i in list_of_h:
        for ind,val in enumerate(solve(i)):
            df.loc[rows[ind],i]=val
        print(f'{i} completed') 
        display(df.round(2))
        RNode=None
        return df


# In[91]:


def start_assignment(): 
    global start,initialMatrix 
    scanned_list=list(map(int,input("Enter custom start matrix with spaces in same line(put 0 in place of blank)\n").strip().split())) 
    initialMatrix=scanned_list[:]
    scanned_list[scanned_list.index(0)]=' '
    result=check_solvability(copy.deepcopy(scanned_list))
    start=[scanned_list[0:3],scanned_list[3:6],scanned_list[6:]] 
    for i,j,k in start:print(i,j,k)
    if(result):
        Assignment()
start_assignment()


# In[ ]:




