import copy
import random
import math

# let there be 7 nodes
# distance of each node
# from each other is given
# along with max speed limit 
# on each path.

# the amount of traffic between
# each path will be entered during
# the runtime and time for travesal
# of each node will be calculated by 
# algo and path taking least time will
# be returned

# distance in meters
graph=[[0,1100,0,0,1800,0,0],
       [1100,0,1500,0,0,0,0],
       [0,1500,0,900,700,0,1700],
       [0,0,900,0,400,1000,0],
       [1800,0,700,400,0,0,0],
       [0,0,0,1000,0,0,200],
       [0,0,1700,0,0,200,0]]

for i in graph:
    print(i)

#taking input from user starting and goal node
start=int(input('enter the starting node(1 indexed):-')) 
goal=int(input('enter the goal node(1 indexed):-')) 


#checking the validation of the input
if(not (start>0 and start<=len(graph[0])) or not (goal>0 and goal<=len(graph[0]))):
    exit("#######################################################WRONG START OR GOAL NODE#######################################################")

#Function to calculate time in seconds to travel from a node to another on basis on speed limit on each road 
def time():
    for i in range(0,len(graph[0])):
        for j in range(0,len(graph[0])):
            if(graph[i][j]!=0):
                temp=graph[i][j]/speedlimit(i,j)
                graph[i][j]=temp

# speedlimit on each road in metre per sec
def speedlimit(a,b):     
    h={(0,1):80,(1,0):80,(0,4):60,(4,0):60,
       (1,2):50,(2,1):50,
       (2,3):45,(3,2):45,(2,4):30,(4,2):30,
       (2,6):90,(6,2):90,
       (3,4):15,(4,3):15,(3,5):50,(5,3):50,
       (5,6):10,(6,5):10}     
    return h[(a,b)]

time()

#taking the input of time delay in seconds due to traffic on each road
# def trafficinput():
#     for i in range(0,len(graph[0])):
#             for j in range(0,len(graph[0])):
#                 if(graph[i][j]!=0 and i<=j):
#                     print("enter the time delay due to traffic between road",i+1,"and",j+1)
#                     temp=int(input())
#                     graph[i][j]+=temp
#                     graph[j][i]+=temp

def trafficinput():
    for i in range(0,len(graph[0])):
            for j in range(0,len(graph[0])):
                if(graph[i][j]!=0 and i<=j):
                    temp=random.randint(0,100)
                    print("enter the time delay due to traffic between road",i+1,"and",j+1,"=",temp)
                    graph[i][j]+=temp
                    graph[j][i]+=temp

trafficinput()

population=[]
visited=[]

#Creating an initial population
def populationcreator(population,start,goal):
    for i in range(0,4):
        while True:
            temp=randomlist(start,goal)
            if geneisfit(temp):
                break
        if temp not in population:   
            population.append(temp)

#Checking if a gene is fit or not
def geneisfit(list):
    prev=list[0]
    for i in range(1,len(list)):
        if graph[prev-1][list[i]-1]==0:
            return False
        else:
            prev=list[i]
    return True

#Calculating the fittness value of a gene 
def fittness(list):
    cost=0
    prev=list[0]
    for i in range(1,len(list)):
        cost+=graph[prev-1][list[i]-1]
        prev=list[i]
    return cost

#implimenting genetic algorithm
def geneticalgo(iteration,population,count,visited):
    populationcreator(population,start,goal)
    i=0
    while i<len(population):
        temp=fittness(population[i])
        visited.append(population[i])
        population[i]=[temp,count,population[i]]
        count+=1
        i+=1
    i=0
    while(i<iteration):
        population.sort()
        crossover(population,count)
        mutation(count)
        i+=1
    population.sort()
    print("#######################################################SUCCESS#######################################################")
    print("Time =",fittness(population[0][2]))
    print("Path to take to reach your destination from current node:-")
    for node in population[0][2]:
        print("->",node)

def crossover(population,count):
    if len(population)>1:
        temp1=population[0][2]
        temp2=population[0][2]
    else:
        return
    pt=int(math.ceil(len(temp1)/2))

    child1=temp1[0:pt]+temp2[pt:]
    child2=temp2[0:pt]+temp1[pt:]
    child1=[fittness(child1),count,child1]
    child2=[fittness(child2),count,child2]
    if child1[2] not in visited and geneisfit(child1[2]):
        population+=child1
        visited.append(child1[2])
        count+=1
    if child2[2] not in visited and geneisfit(child2[2]):
        population+=child2
        visited.append(child2[2])
        count+=1

def mutation(count):
    temp=population[-1][2]
    temp1=copy.deepcopy(temp)
    tempvar1=random.randint(1,len(temp1)-1)
    tempvar2=random.randint(1,len(temp1)-1)
    swap=temp1[tempvar1]
    temp1[tempvar1]=temp1[tempvar2]
    temp1[tempvar2]=swap
    if temp1 not in visited and geneisfit(temp1):
        population.append([fittness(temp1),count,temp1])
        visited.append(temp1)
        count+=1
    else:
        temp1=randomlist(start,goal)
        if temp1 not in visited and geneisfit(temp1):
            population.append([fittness(temp1),count,temp1])
            visited.append(temp1)
            count+=1

#Funtion to create a random gene
def randomlist(start,goal):
    list=[]
    visited=[start,goal]
    list.append(start)
    temp=start
    for i in range(0,len(graph[0])-2):
        while True:
            temp=random.randint(1,7)
            if temp not in visited:
                visited.append(temp)
                break
        if random.uniform(0,1)<0.5:
            list.append(temp)
    list.append(goal)
    return list
    
geneticalgo(10,population,0,visited)

















