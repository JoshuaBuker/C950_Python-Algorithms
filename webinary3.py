
# C950 - Webinar-3 - How to Dijkstra - Complete Python Code
# Rate This Article	
# (Average Rating: No Rating)
# Show Properties

# C950 - Webinar-3 - How to Dijkstra?
# W-3_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy_Dijkstra.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# Ref: zyBooks: 3.3.1: MakeChange greedy algorithm.
# Ref: zyBooks: zyDE 6.12.1: Dijkstra's shortest path example.
# Ref: Graph Data Structure 4. Dijkstra’s Shortest Path Algorithm: https://www.youtube.com/watch?v=pVfj6mxhdMw 
'''
Add this file to the project
BestMovies.csv:
-----------------------
ID, Name, Year, Price, City, State
1, "CITIZEN KANE", 1941, 25.00, Salt Lake City, Utah
2, "CASABLANCA", 1942, 25.00, Helena, Montana
3, "THE GODFATHER", 1972, 10.00, Santa Fe, New Mexico
4, "GONE WITH THE WIND", 1939, 10.00, Austin, Texas
5, "LAWRENCE OF ARABIA", 1962, 10.00, Lincoln, Nebraska
6, "THE WIZARD OF OZ", 1939, 10.00, Madison, Wisconsin
7, "THE GRADUATE", 1967, 5.00, New York, New York
8, "ON THE WATERFRONT", 1954, 5.00, Columbus, Ohio
9, "SCHINDLER'S LIST", 1993, 5.00, Raleigh, North Carolina
10, "SINGIN' IN THE RAIN", 1952, 5.00, Orlando, Florida
11, "STAR WARS", 1977, 1.00, Montgomery, Alabama
-----------------------
'''
import csv
import math
 
# HashTable class using chaining - START
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
      
    # Inserts a new item into the hash table.
    def insert(self, key, item): #  does both insert and update 
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
 
        # update key if it is already in the bucket
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
            kv[1] = item
            return True
        
        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True
 
    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #print(bucket_list)
 
        # search for the key in the bucket list
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
            return kv[1] # value
        return None
 
    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
 
        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
              bucket_list.remove([kv[0],kv[1]])
# HashTable class using chaining - END
 
# Movie CSV Data import - START
class Movie:
    def __init__(self, ID, name, year, price, city, state, status):
        self.ID = ID
        self.name = name
        self.year = year
        self.price = price
        self.city = city
        self.state = state
        self.status = status
    
    def __str__(self):  # overwite print(Movie) otherwise it will print object reference 
        return "%s, %s, %s, %s, %s, %s, %s" % (self.ID, self.name, self.year, self.price, self.city, self.state, self.status)  
 
def loadMovieData(fileName):
    with open(fileName) as bestMovies:
        movieData = csv.reader(bestMovies, delimiter=',')
        next(movieData) # skip header
        for movie in movieData:
            mID = int(movie[0])
            mName = movie[1]
            mYear = movie[2]
            mPrice = movie[3]
            mCity = movie[4]
            mState = movie[5]
            mStatus = "Loaded"
           
            # movie object
            m = Movie(mID, mName, mYear, mPrice, mCity, mState, mStatus)
            #print(m)
 
            # insert it into the hash table
            myHash.insert(mID, m)
 
# Hash table instance 
myHash = ChainingHashTable()
 
# Load movies to Hash Table
loadMovieData('BestMovies.csv');
 
print("BestMovies from Hashtable:")
# Fetch data from Hash Table
for i in range (len(myHash.table)+1): 
    print("Movie: {}".format(myHash.search(i+1))) # 1 to 11 is sent to myHash.search()
# Movie CSV Data import - END
 
# Greedy Algorithm - START
# Greedy Algorithm: Min Expenses => Max Profits
def greedyAlgorithmMinExpenses(budget):
    total = budget
    c25dollar = 0
    c10dollar = 0
    c5dollar = 0
    c1dollar = 0
    while (budget >= 25):
        if c25dollar > 3: # why 3? 0,1,2,3 will not break so 4 times.
            break
        c25dollar += 1
        budget = budget - 25
    while (budget >= 10):
        c10dollar += 1
        budget = budget - 10
    while (budget >= 5):
        c5dollar += 1
        budget = budget - 5
    while (budget > 0):
        if c1dollar > 3:
            break
        c1dollar += 1
        budget = budget - 1
    
    cDVDs = c25dollar + c10dollar + c5dollar + c1dollar
    
    # expense calculation
    eDVDs = 1.00 * cDVDs # Material cost of DVD: $1.00
    eLabor = 12.00 * (math.ceil(cDVDs/10)) # Labor is $12.00 for every 10 DVDs, $24.00 for 11 DVDs
    eShipping = 0.50 * cDVDs # Shipping cost is $0.50 per DVD
    eTotal = eDVDs + eLabor + eShipping
    profit = total - eTotal
 
    print("${:.2f}-Budget, {}-DVDs, ${:.2f}-Expense, ${:.2f}-Profit ==>".format(total,cDVDs,eTotal,profit))
    print(" {} x 25 dollar movie = ${:.2f}".format(c25dollar,c25dollar*25.00))
    print(" {} x 10 dollar movie = ${:.2f}".format(c10dollar,c10dollar*10.00))
    print(" {} x 5  dollar movie = ${:.2f}".format(c5dollar,c5dollar*5.00))
    print(" {} x 1  dollar movie = ${:.2f}".format(c1dollar,c1dollar*1.00))
 
print("\nGreedy Algorithm: Min Expenses => Max Profits")
greedyAlgorithmMinExpenses(102) # $102.00 budget 
greedyAlgorithmMinExpenses(94) # $94.00 budget
greedyAlgorithmMinExpenses(71) # $71.00 budget
greedyAlgorithmMinExpenses(200) # $200.00 budget
# Greedy Algorithm - END
 















 
# Dijkstra shortest path - START
class Vertex:
    # Constructor for a new Vertx object. All vertex objects
    # start with a distance of positive infinity.
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.pred_vertex = None
        
class Graph:
    def __init__(self):
        self.adjacency_list = {} # vertex dictionary {key:value}
        self.edge_weights = {} # edge dictionary {key:value}
        
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = [] # {vertex_1: [], vertex_2: [], ...}
        
    def add_directed_edge(self, from_vertex, to_vertex, weight = 1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight 
            # {(vertex_1,vertex_2): 484, (vertex_1,vertex_3): 626, (vertex_2,vertex_6): 1306, ...}
        self.adjacency_list[from_vertex].append(to_vertex) 
            # {vertex_1: [vertex_2, vertex_3], vertex_2: [vertex_6], ...}
 
    def add_undirected_edge(self, vertex_a, vertex_b, weight = 1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)
 
# Dijkstra shortest path
def dijkstra_shortest_path(g, start_vertex):
    # Put all vertices in an unvisited queue.
    unvisited_queue = []
 
    for current_vertex in g.adjacency_list:
        unvisited_queue.append(current_vertex) 
            # unvisited_queue = [vertex_1, vertex_2, ...]
 
    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0
 
    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while len(unvisited_queue) > 0:
        
        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            #print(unvisited_queue[i].label, unvisited_queue[i].distance, unvisited_queue[i].pred_vertex)
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)
        #print("From Start Vetex to current_vertex.label: " + current_vertex.label +" distance: " + str(current_vertex.distance))
 
        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]: # values from  dictionary
                # if current_vertex = vertex_1 => adj_vertex in [vertex_2, vertex_3], if vertex_2 => adj_vertex in [vertex_6], ...
            edge_weight = g.edge_weights[(current_vertex, adj_vertex)] # values from dictionary
                # edge_weight = 484 then 626 then 1306, ...}
            alternative_path_distance = current_vertex.distance + edge_weight
                        
            # If shorter path from start_vertex to adj_vertex is found, update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex
                
def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        path = " -> " + str(current_vertex.label) + path
        current_vertex = current_vertex.pred_vertex
    path = start_vertex.label + path
    return path
 
def get_shortest_path_city(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        myMovie = myHash.search(int(current_vertex.label))
        path = " -> " + myMovie.city + path
        current_vertex = current_vertex.pred_vertex
    path = "Salt Lake City " + path
    return path
 
# Dijkstra shortest path main 
# Program to find shortest paths from vertex A.
g = Graph()
 
# add Vertices
vertex_1 = Vertex("1") # 1, "CITIZEN KANE", 1941, 25.00, Salt Lake City, Utah
g.add_vertex(vertex_1)
vertex_2 = Vertex("2") # 2, "CASABLANCA", 1942, 25.00, Helena, Montana
g.add_vertex(vertex_2)
vertex_3 = Vertex("3") # 3, "THE GODFATHER", 1972, 10.00, Santa Fe, New Mexico
g.add_vertex(vertex_3) 
vertex_4 = Vertex("4") # 4, "GONE WITH THE WIND", 1939, 10.00, Austin, Texas
g.add_vertex(vertex_4) 
vertex_5 = Vertex("5") # 5, "LAWRENCE OF ARABIA", 1962, 10.00, Lincoln, Nebraska
g.add_vertex(vertex_5) 
vertex_6 = Vertex("6") # 6, "THE WIZARD OF OZ", 1939, 10.00, Madison, Wisconsin
g.add_vertex(vertex_6) 
vertex_7 = Vertex("7") # 7, "THE GRADUATE", 1967, 5.00, New York, New York
g.add_vertex(vertex_7) 
vertex_8 = Vertex("8") # 8, "ON THE WATERFRONT", 1954, 5.00, Columbus, Ohio
g.add_vertex(vertex_8) 
vertex_9 = Vertex("9") # 9, "SCHINDLER'S LIST", 1993, 5.00, Raleigh, North Carolina
g.add_vertex(vertex_9) 
vertex_10 = Vertex("10") # 10, "SINGIN' IN THE RAIN", 1952, 5.00, Orlando, Florida
g.add_vertex(vertex_10) 
vertex_11 = Vertex("11") # 11, "STAR WARS", 1977, 1.00, Montgomery, Alabama
g.add_vertex(vertex_11) 
 
# add Edges 
g.add_undirected_edge(vertex_1, vertex_2, 484) # 484 miles
g.add_undirected_edge(vertex_1, vertex_3, 626)
g.add_undirected_edge(vertex_2, vertex_6, 1306)
g.add_undirected_edge(vertex_3, vertex_5, 774)
g.add_undirected_edge(vertex_3, vertex_4, 687)
g.add_undirected_edge(vertex_4, vertex_11, 797)
g.add_undirected_edge(vertex_5, vertex_6, 482)
g.add_undirected_edge(vertex_6, vertex_7, 936)
g.add_undirected_edge(vertex_7, vertex_8, 535)
g.add_undirected_edge(vertex_7, vertex_9, 504)
g.add_undirected_edge(vertex_9, vertex_10, 594)
g.add_undirected_edge(vertex_11, vertex_5, 970)
g.add_undirected_edge(vertex_11, vertex_8, 664)
g.add_undirected_edge(vertex_11, vertex_9, 567)
g.add_undirected_edge(vertex_11, vertex_10, 453)
 
# Run Dijkstra's algorithm first.
dijkstra_shortest_path(g, vertex_1)
 
# Get the vertices by the label for convenience; display shortest path for each vertex
# from vertex_1.    
print("\nDijkstra shortest path:")
for v in g.adjacency_list:
    if v.pred_vertex is None and v is not vertex_1:
        print("1 to %s ==> no path exists" % v.label)
    else:
        print("1 to %s ==> %s (total distance: %g)" % (v.label, get_shortest_path(vertex_1, v), v.distance))
 
print("\nDijkstra shortest path with Cities:")
for v in g.adjacency_list:
    myMovie = myHash.search(int(v.label))
    if v.pred_vertex is None and v is not vertex_1:
        print("Salt Lake City to %s ==> no path exists" % myMovie.city)
    else:
        print("Salt Lake City to %s ==> %s (total distance: %g)" % (myMovie.city, get_shortest_path_city(vertex_1, v), v.distance))
# Dijkstra shortest path - END
 



# Article Link: 
# https://srm--c.vf.force.com/apex/coursearticle?Id=kA03x000000e1gECAQ
