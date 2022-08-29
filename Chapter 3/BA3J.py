# -*- coding: utf-8 -*-
"""BA3J.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ra0ZtuYmVoUqGxoetwRuGIoE4a7gcVoH
"""

def eulerianCycle(graph):
    
    cycle = [list(graph.keys())[0]]
    
    while (len(graph) > 0):

        if cycle[0] == cycle[-1]:

            while not cycle[0] in graph:
                cycle.pop(0)
                cycle.append(cycle[0])
          
        start = cycle[-1]
        
        cycle.append(graph[start].pop())  
        if len(graph[start]) == 0: del graph[start]
       
    return cycle


def eulerianPath(graph):

    # find the unbalanced nodes
    balances = {}

    # set values of all nodes in graph to 0
    for key in graph.keys():
        for element in graph[key]:
            if element not in balances.keys():
                balances[element] = 0
        if key not in balances.keys():
            balances[key] = 0
    
    for sourceNode in graph.keys():
        for targetNode in graph[sourceNode]:

            # finding the difference between indegree and outdegree:
            # +1 for every time you enter this node ( -> node)
            balances[targetNode] += 1
            # -1 for every time you leave this node ( node -> )
            balances[sourceNode] -= 1
            
    
    for node in balances:

        # if you can leave a node but can't enter it:
        if balances[node] == -1:
            targetNode = node
        # if you can enter a node but can't leave it:
        if balances[node] == 1:
            sourceNode = node

    # add the missing edge
    if sourceNode in graph.keys():
        graph[sourceNode].append(targetNode)
    else:
        graph[sourceNode] = [targetNode]

    # run eulerianCycle and drop the circle closing postfix
    path = eulerianCycle(graph)[0:-1]

    # rotate until the missing edge matches end and beginning
    while path[0] != targetNode or path[-1] != sourceNode:  
       path.append(path.pop(0))
       
    return path

'''________________________________________________________________________'''


def StringReconstructionFromReadPairs(k, d, pairs):
    graph = DeBruinGraphFromReadPairs(pairs)
    path = eulerianPath(graph)

    # glue all the firsts in pairs
    text = path[0][0]
    for i in range (1,len(path)):
        text += path[i][0][-1]
    # add the remaining (k+d)-mer
    for i in range(len(path) - d - 2, len(path) - 1):
        text += path[i][1][0]
    text += path[-1][1]
        
    return text


def DeBruinGraphFromReadPairs(pairs):
    graph = dict()
    for pair in pairs:
        prefix = (pair[0][:-1], pair[1][:-1])
        postfix = (pair[0][1:], pair[1][1:])
        
        if prefix in graph:
            graph[prefix].append(postfix)
        else:
            graph[prefix] = [postfix]
            
    return graph


with open("rosalind_ba3j.txt") as file:
    lines = file.readlines()


k = int(lines[0].strip('\n').split(' ')[0])
d = int(lines[0].strip('\n').split(' ')[1])

for i in range (1,len(lines)):
    lines[i] = lines[i].strip("\n").split('|')
    
print(StringReconstructionFromReadPairs(k, d, lines[1:]))