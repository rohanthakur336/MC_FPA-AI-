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
closed=q.PriorityQueue()
visited=[start]
cl=[]
open.put([graph[start][start]+heuristic(start),graph[start][start],start,None])

#implimenting A*
def astar():
    while not open.empty():
        temp=open.get() 
        visited.remove(temp[2])
        closed.put(temp)
        cl.append(temp[2])
        if temp[2]==goal:
            print('#######################################################SUCCESS#######################################################')
            resultlist(closed,temp[3],goal)
            return
        else:
            list=[i for i in range(0,len(graph[0])) if graph[temp[2]][i]!=0]
            for next in list:
                cost=temp[1]+graph[temp[2]][next]
                fn=cost+heuristic(next)
                if next not in visited and next not in cl:
                    open.put([fn,cost,next,temp[2]])
                    visited.append(next)
                if next in visited:
                    updateopen(next,fn,cost,temp[2])
                if next in cl:
                    updateclosed(next,fn,cost,temp[2])

def updateopen(next,fn,cost,parent):
    temp=open.get()
    if temp[2]==next:
        if cost<temp[1]:
            open.put([fn,cost,next,parent])
        else:
            open.put(temp)
        return
    updateopen(next,fn,cost,parent)
    open.put(temp)

def updateclosed(next,fn,cost,parent):
    templist=[]
    while 1:
        temp=closed.get()
        if temp[2]==next:
            if cost<temp[1]:
                closed.put([fn,cost,next,parent])
                for i in templist:
                    closed.put(i)
                propogateimprovement(temp[2],cost)
            else:
                closed.put(temp)
                for i in templist:
                    closed.put(i)
            break
        else:
            templist.append(temp)
    
    
def propogateimprovement(next,cost):
    list=(i for i in range(0,len(graph[0])) if graph[next][i]!=0)
    for each in list:
        costnew=cost+graph[next][each]
        fnnew=costnew+heuristic(each)
        if each in visited:
            updateopen(each,fnnew,costnew,next)
        if each in cl:
            updateclosed(each,fnnew,costnew,next)


def resultlist(closed,parent,goal):
    result=[]
    while not closed.empty():
        temp=closed.get()
        result.append(temp)
    print("Time =",result[len(result)-1][1])
    print("Path to take to reach your destination from current node:-")
    pathgenerator(result,parent,goal)
    
#generating path from start to goal node
def pathgenerator(closed,parent,goal):
    if parent==None:
        print('->',goal)
        return
    for i in closed:
        if i[2]==goal:
            for j in closed:
                if j[2]==i[3]:
                    pathgenerator(closed,j[3],j[2])
                    print('->',i[2])
                    return
                
astar()


                