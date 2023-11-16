from enum import Enum
from datetime import time
import csv

# ============================== STATUS ENUM =================================
class Status(Enum):
    HUB = "at the Hub"
    TRANSIT = "in transit"
    DELIVERED = "delivered"


# ============================= HASH TABLE CLASS =============================
class HashMap:
    def __init__(self):
        self.size = 64
        self.map = []
        for i in range(self.size):
            self.map.append([])
    
    def add(self, key, value):
        kh = hash(key) % self.size

        if (self.map[kh] is None):
            self.map[kh] = list([[key, value]])
            return True
        else:
            for pair in self.map[kh]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[kh].append([key, value])
            return True
    
    def get(self, key):
        kh = hash(key) % self.size
        if (self.map[kh] is not None):
            for pair in self.map[kh]:
                if pair[0] == key:
                    return pair[1]
        return None
    
    def delete(self, key):
        kh = hash(key) % self.size

        if (self.map[kh] is None):
            return False
        for i in range (0, len(self.map[kh])):
            if self.map[kh][i][0] == key:
                self.map[kh].pop(i)
                return True
    
    def print(self):
        for item in self.map:
            if item is not None:
                if item:
                    print(str(item))

# ============================== GRAPH CLASS =================================
class Graph():
    def __init__(self, file):
        graphPair = self.loadCSV(file)

        self.graph = graphPair[0]
        self.V = graphPair[1]
        self.visited = [None]*self.V

    def loadCSV(self, file):
        graphArray = []
        counter = 0
        index = 0
        with open(file, newline='') as csvFile:
            rd = csv.reader(csvFile, delimiter=',')
            for row in rd:
                if (counter >= 1):
                    address = row[1].split("(")[0].strip()
                    Location.LocationMap.add(index, Location(address, False))
                    Location.LocationToIDMap.add(address, index)
                    graphArray.append(row[2:])
                    index += 1
                else:
                    counter += 1

        length = len(graphArray)
            
        graphArray[0][0] = float(graphArray[0][0])
        for i, arr in enumerate(graphArray):
            for j in range(i+1):
                graphArray[i][j] = float(graphArray[i][j])
                graphArray[j][i] = graphArray[i][j]
        graphArray[length-1][length-1] = float(graphArray[length-1][length-1])

        return [graphArray, length]
    
    def minDistance(self, dist, sptSet):
        min = 1e7
 
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
    
    def DistanceToAllPoints(self, src):
        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                    sptSet[v] == False and
                    dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]

        return dist
    
    def DistanceToPoint(self, src, end):
        return self.DistanceToAllPoints(src)[end]
    
    def NearestPointFrom(self, src, map):
        min = 1e7
        min_index = None

        for i, val in enumerate(self.graph[src]):
            if (i is not src and val < min and map.get(i).visited == False):
                min = val
                min_index = i
        
        if (min == 1e7):
            return False
        else:
            return [min_index, min]



# ============================= PACKAGE CLASS ================================
class Package():
    PackageMap = HashMap()

    def __init__(self, deadline, address, city, zipCode, weight, specialNotes):
        self.deadline = deadline
        self.address = address
        self.city = city
        self.zipcode = zipCode
        self.weight = weight
        self.status = Status.HUB
        self.timeLoaded = None
        self.timeDelivered = None
        self.specialNotes = specialNotes

    def setStatus(self, status, currentTime): 
        self.status = status

        if (status == Status.TRANSIT):
            self.timeLoaded = currentTime
        elif (status == Status.DELIVERED):
            self.timeDelivered = currentTime
    
# ============================= LOCATION CLASS ===============================
class Location():
    LocationMap = HashMap()
    LocationToIDMap = HashMap()

    def __init__(self, address, visited):
        self.address = address
        self.visited = visited
    
    def setVisited(self, visited):
        self.visited = visited

# =============================== TRUCK CLASS ================================
class Truck():
    def __init__(self, label):
        self.label = label
        self.path = {}
        self.packages = {}
        self.currentLocation = Location.IDToLocationMap.get(0)
        self.clock = time(8, 00, 00)
        self.packageMap = Package.PackageMap
        self.IDToLocationMap = Location.IDToLocationMap
        self.locationToIDMap = Location.LocationToIDMap
    
    def setPath(self, path):
        self.path = path
    
    def load(self, packages):
        self.packages = packages