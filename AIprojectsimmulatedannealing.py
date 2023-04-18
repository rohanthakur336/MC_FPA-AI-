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

#taking input from user starting and goal node
start=int(input('enter the starting node(1 indexed):-')) 
goal=int(input('enter the goal node(1 indexed):-')) 

#checking the validation of the input
if(not (start>=1 and start<=len(graph[0])) or not (goal>0 and goal<=len(graph[0]))):
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

#Calculating the fittness value of a gene 
def fittness(list):
    cost=0
    prev=list[0]
    for i in range(1,len(list)):
        cost+=graph[prev-1][list[i]-1]
        prev=list[i]
    return cost

#Checking if a gene is fit or not
def geneisfit(list):
    prev=list[0]
    for i in range(1,len(list)):
        if graph[prev-1][list[i]-1]==0:
            return False
        else:
            prev=list[i]
    return True

#Calculating the probability whether a gene will be accepted as current or not
def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)
    
#implementing simulated annealing
def simulated_annealing(order,start,goal,initial_temperature=10000, cooling_rate=0.99, num_iterations=1000):
    current_order = order
    best_order = current_order
    current_cost = fittness(current_order)
    best_cost = current_cost
    temperature = initial_temperature
    for i in range(num_iterations):
        new_order=[]
        while True:
            new_order =randomlist(start,goal)
            if geneisfit(new_order):
                break
        new_cost = fittness(new_order)
        ap = acceptance_probability(current_cost, new_cost, temperature)
        if ap > random.random():
            current_order = new_order
            current_cost = new_cost
        if current_cost < best_cost:
            best_order = current_order
            best_cost = current_cost
        temperature *= cooling_rate
    return [best_order, best_cost]

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

order=[]
while True:
    order =randomlist(start,goal)
    if geneisfit(order):
        break

list= simulated_annealing(order,start,goal)
print("#######################################################SUCCESS#######################################################")
print("Time =", list[1])
print("Path to take to reach your destination from current node:-")
for node in list[0]:
    print("->",node)

