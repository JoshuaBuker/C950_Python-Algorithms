import csv


# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph
class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[None]*vertices for i in range(vertices)]
        self.visited = [None]*vertices
 
    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = 1e7
 
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src, end):
 
        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                   sptSet[v] == False and
                   dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
 
        return dist[end]

graphArray = []
counter = 0
with open('WGUPS Distance Table.csv', newline='') as csvFile:
    rd = csv.reader(csvFile, delimiter=',')
    for row in rd:
        if (counter >= 1):
            graphArray.append(row[2:])
        else:
            counter += 1

length = len(graphArray)
    
graphArray[0][0] = float(graphArray[0][0])
for i, arr in enumerate(graphArray):
    for j in range(i+1):
        graphArray[i][j] = float(graphArray[i][j])
        graphArray[j][i] = graphArray[i][j]
graphArray[length-1][length-1] = float(graphArray[length-1][length-1])

g = Graph(length)
g.graph = graphArray

# print(*g.graph, sep='\n')
print(g.dijkstra(0, 1))
# print(g.V)
print(g.visited)
        