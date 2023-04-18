import queue as q
import math as m
import random

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

#heuristic based on distance of current node from goal node
def heuristic(state):
    list1=coordinate(state)
    list2=coordinate(goal)
    temphue=m.sqrt((list1[0]-list2[0])**2+(list1[1]-list2[1])**2)
    return temphue

#coordinates of each node
def coordinate(state):
        list=[[0,0],[8,6],[22,7],[15,12],[15.7,8.5],[6,8],[5,7]]
        return list[state]

#taking input from user starting and goal node
start=int(input('enter the starting node(0 indexed):-')) 
goal=int(input('enter the goal node(0 indexed):-')) 


#checking the validation of the input
if(not (start>=0 and start<len(graph[0])) or not (goal>=0 and goal<len(graph[0]))):
    exit("#######################################################WRONG START OR GOAL NODE#######################################################")

time()   

#taking the input of time delay in seconds due to traffic on each road
# def trafficinput():
#     for i in range(0,len(graph[0])):
#             for j in range(0,len(graph[0])):
#                 if(graph[i][j]!=0 and i<=j):
#                     print("enter the time delay due to traffic between road",i,"and",j)
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

open=q.PriorityQueue()
open.put([heuristic(start),0,start,None])
visited=[start]
closed=[]

#implimenting bestfirstsearch
def bestfirstsearch(open,count):
    while not open.empty():
        temp=open.get()
        closed.append([temp[2],temp[3]])
        if temp[2] not in visited:
            visited.append(temp[2])
        if temp[2]==goal:
            print("#######################################################SUCCESS#######################################################")
            pathgenerator(closed,temp[3],goal,graph[temp[3]][goal])
            return
        else:
            list=[i for i in range(0,len(graph[0])) if graph[temp[2]][i]!=0]
            for next in list:
                if next not in visited:
                    visited.append(next)
                    open.put([heuristic(next),count,next,temp[2]])
                    count+=1

#generating path from start to goal node
def pathgenerator(closed,parent,goal,cost):
    if parent==None:
        print('TIME =',cost)
        print("Path to take to reach your destination from current node:-")
        print('->',goal)
        return
    for i in closed:
        if i[0]==goal:
            for j in closed:
                if j[0]==i[1]:
                    if j[1]!=None:
                        cost=cost+graph[j[1]][j[0]]
                    pathgenerator(closed,j[1],j[0],cost)
                    print('->',i[0])
                    return

bestfirstsearch(open,1)

# for i in range(0,len(graph[0])):
#     print(heuristic(i)," ")


