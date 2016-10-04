# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    g = WeightedDigraph()
    path = 'D:/Documents/edX/ProblemSet5/' + mapFilename
    f = open(path,'r')
    data = f.readline()
    while data:
        n1,n2,d1,d2 = data.split(' ')
        na = Node(n1)
        nb = Node(n2)
        if not g.hasNode(na):
            g.addNode(na)
        if not g.hasNode(nb):
            g.addNode(nb)
        e1 = WeightedEdge(na,nb,d1,d2)
        g.addEdge(e1)
        data = f.readline()
    #print "Loading map from file...", path
    #print d
    f.close()
    return g

        

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

#def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
#    pass
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    
    start = Node(start)
    end = Node(end)
    #print digraph
    outputs = dfsValidPathsBF(digraph,start,end,path=[],validPaths=[])
    #validPaths = outputs[1]
    #print outputs[1]
    #print digraph
    shortestPath = findShortestPath(outputs,maxTotalDist,maxDistOutdoors)
    
    if shortestPath:
        return shortestPath
    else:
        raise ValueError('No shortest path found')

def dfsValidPathsBF(agraph,start,end,path=[],validPaths=[],dist=0.0,out=0.0):
    newPath = []
    path = path + [[start,(dist,out)]]
    if start == end:
        return (path,validPaths)
    for node_info in agraph.edges[start]:
        node = node_info[0]
        aPath = [item[0] for item in path]
        if node not in aPath:
            dist,out = node_info[1]
            temp = dfsValidPathsBF(agraph,node,end,path,validPaths,dist,out)
            newPath = temp[0]
            if newPath and newPath not in validPaths:
                validPaths.append(newPath)
        else:
            pass
    return (newPath,validPaths)

def findShortestPath(outputs,shortTot,shortOut):
    minOutPath = []
    for path in outputs[1]:
        totdist = 0.0
        outdist = 0.0
        for edge in path:
            dist,out = edge[1]
            totdist += dist
            outdist += out
        if outdist <= shortOut and totdist <= shortTot:
            minOutPath.append((path,totdist))
    if minOutPath:
        shortestPath = min(minOutPath, key = lambda t: t[1])        
        final_output = []
        for node in shortestPath[0]:
            final_output = final_output + [node[0].getName()]
        return final_output
    else:
        return minOutPath

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO    
    start = Node(start)
    end = Node(end)
    #print digraph
    shortestPath,tot,out = dfsValidPaths(digraph,start,end,maxTotalDist,maxDistOutdoors)
    #print tot,out
    if shortestPath:
        return [node[0].getName() for node in shortestPath]
    else:
        raise ValueError('No shortest path found')
        
def dfsValidPaths(agraph,start,end,maxDist,maxOut,currentPath=[],shortestPath=(),curDist=0,curOut=0):
    if not currentPath:
        start = [start,(0,0)]
    currentPath = currentPath + [start]
        
    growPath = findDistances(currentPath,curDist,curOut,maxDist,maxOut)
    #print currentPath,growPath,curDist,curOut,maxDist,maxOut,'-2'
    if growPath[0]:
        if start[0] == end:
            curDist,curOut = growPath[1]
            return currentPath,curDist,curOut
        for node_info in agraph.edges[start[0]]:
            node = node_info[0]
        #print node,'-3'
            aPath = [item[0] for item in currentPath]
            if node not in aPath:
                shortestPath,curDist,curOut = dfsValidPaths(agraph,node_info,end,maxDist,maxOut,
                                                            currentPath,shortestPath,curDist,curOut)
            #print shortestPath, '-4'
            else:
                pass
            #print node
    #print shortestPath,maxDist,maxOut
    return shortestPath,curDist,curOut

def findDistances(activePath,curDist,curOut,maxDist,maxOut):
    if curDist == 0 and curOut == 0:
        curDist,curOut = maxDist,maxOut
    totdist = 0.0
    outdist = 0.0
    #print activePath,'-1'
    for edge in activePath:
        dist,out = edge[1]
        totdist += dist
        outdist += out
    if totdist <= curDist:
        if outdist <= curOut:
            return (True,(totdist,outdist))
        elif outdist > curOut and outdist <= maxOut:
            return (True,(totdist,outdist))
        else:
            return (False,(totdist,outdist))
    else:
        return (False,(totdist,outdist))

#Uncomment below when ready to test
### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
 #   Test cases
    mitMap = load_map("mit_map.txt")
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges


    LARGE_DIST = 1000000

 #   Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
#    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
#    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1
    #print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

    #Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
#    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
#    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
#    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
#    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
#    brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
#    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
#    brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
#    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#    brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
#    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
#    try:
#        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
#    except ValueError:
#        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
#    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

#    Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
#    try:
#        bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#    except ValueError:
#        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
#    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr
