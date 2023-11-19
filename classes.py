from enum import Enum
from datetime import *
import csv

# ============================== STATUS ENUM =================================
class Status(Enum):
    HUB = "at the Hub"
    TRANSIT = "in transit"
    DELIVERED = "delivered"


# ============================= HASH TABLE CLASS =============================
class HashMap:
    def __init__(self):
        self.size = 20
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
                    addressSplit = address.split(" ")
                    for i, str in enumerate(addressSplit):
                        match str:
                            case "North": addressSplit[i] = "N"
                            case "East": addressSplit[i] = "E"
                            case "South": addressSplit[i] = "S"
                            case "West": addressSplit[i] = "W"
                    address = " ".join(addressSplit)
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
    
    def generatePath(self, src, numOfPackages):
        path = {}
        currentLocation = src
        Location.LocationMap.get(currentLocation).setVisited(True)

        for i in range(numOfPackages):
            coords = self.NearestPointFrom(currentLocation, Location.LocationMap)

            if (coords is not False):
                path[i] = coords
                Location.LocationMap.get(coords[0]).setVisited(True)
                currentLocation = coords[0]
            else:
                homeDist = self.DistanceToPoint(currentLocation, 0)
                path[i] = [0, homeDist]
                return path
        homeDist = self.DistanceToPoint(currentLocation, 0)
        path[i] = [0, homeDist]

        return path



# ============================= PACKAGE CLASS ================================
class Package():
    PackageMap = HashMap()

    def __init__(self, id, address, city, state, zipCode, deadline, weight, specialNotes):
        self.id = id
        self.deadline = deadline
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipCode
        self.weight = weight
        self.status = Status.HUB
        self.timeLoaded = 0
        self.timeDelivered = 0
        self.specialNotes = specialNotes
        self.deliveredBy = False

    @staticmethod
    def loadCSV(file):
        counter = 0
        with open(file, newline='') as csvFile:
            rd = csv.reader(csvFile, delimiter=',')
            for row in rd:
                # print(row)
                if (counter >= 1):
                    address = row[1].split("(")[0].strip()
                    addressSplit = address.split(" ")
                    for i, str in enumerate(addressSplit):
                        match str:
                            case "North": addressSplit[i] = "N"
                            case "East": addressSplit[i] = "E"
                            case "South": addressSplit[i] = "S"
                            case "West": addressSplit[i] = "W"
                    address = " ".join(addressSplit)
                    Package.PackageMap.add(int(row[0]), Package(row[0], address, row[2], row[3], row[4], row[5], row[6], row[7]))
                else:
                    counter += 1

    def setStatus(self, status, currentTime, truck): 
        self.status = status
        self.deliveredBy = truck.label

        match status:
            case Status.DELIVERED:
                self.timeDelivered = currentTime.time()
            case Status.TRANSIT:
                self.timeLoaded = currentTime.time()

    def print(self):
        print("{0:3} {1:40} {2:20} {3:6} {4:10} {5:8} {6:12} {7:16} {8:16} {9:20} {10:16}".format(
            self.id,
            self.address,
            self.city,
            self.state,
            self.zipcode,
            self.weight,
            self.deadline,
            self.timeLoaded.strftime('%H:%M'),
            self.timeDelivered.strftime('%H:%M'),
            self.status,
            self.deliveredBy
        ))
    
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
    mph = (1/18)

    def __init__(self, label, start):
        self.label = label
        self.path = []
        self.packages = []
        self.currentLocation = Location.LocationToIDMap.get("HUB")
        self.clock = datetime.strptime(start, '%H:%M:%S')
        self.packageMap = Package.PackageMap
        self.IDToLocationMap = Location.LocationMap
        self.locationToIDMap = Location.LocationToIDMap

    def setPath(self, path):
        self.path = path
    
    def load(self, packages):
        self.packages = packages

        for package in self.packages:
            package.setStatus(Status.TRANSIT, self.clock, self)

    def deliverPackages(self, location):
        deliveredPackages = []

        for idx, package in enumerate(self.packages):
            if (package.address == location.address):
                package.setStatus(Status.DELIVERED, self.clock, self)
                # package.print()
                deliveredPackages.append(package)

        return deliveredPackages
    
    def generatePathForPackages(self, graph):
        locations = []
        path = []

        # self.printHeader()

        for i in range (0, len(self.packages)):
            min = 1e7
            min_index = None

            for idx, val in enumerate(self.packages):
                id = Location.LocationToIDMap.get(val.address)
                dist = graph.DistanceToPoint(self.currentLocation, id)
                distComp = dist
                if (str(val.deadline) == "EOD"):
                    distComp += 6

                if (id is not self.currentLocation and distComp < min and Location.LocationMap.get(id).visited == False): # 
                    min = dist
                    min_index = id
            
            if (min_index is not None):
                path.append([min_index, min])
                self.currentLocation = min_index
                Location.LocationMap.get(min_index).setVisited(True)
                timeSpent = timedelta(hours=(Truck.mph * dist))
                self.clock += timeSpent
                # print(timeSpent)
                self.deliverPackages(Location.LocationMap.get(min_index))
                

            else:
                dist = graph.DistanceToPoint(self.currentLocation, 0)
                path.append([0, dist])
                self.currentLocation = 0
                timeSpent = timedelta(hours=(Truck.mph * dist))
                self.clock += timeSpent
                # print(timeSpent)
                self.path = path
                return

        dist = graph.DistanceToPoint(self.currentLocation, 0)
        path.append([0, dist])
        self.currentLocation = 0
        self.clock += timedelta(hours=(Truck.mph * dist))
        self.path = path
        
        
    def getRemainingLocations(self, graph):
        remainingPackages = []
        path = []

        # self.printHeader()

        for i in range(1, 41):
            if (Package.PackageMap.get(i).status == Status.HUB):
                remainingPackages.append(Package.PackageMap.get(i))
        
        self.load(remainingPackages)
        
        while (len(self.packages) > 0):
            min = 1e7
            min_index = None

            for idx, val in enumerate(self.packages):
                id = Location.LocationToIDMap.get(val.address)
                dist = graph.DistanceToPoint(self.currentLocation, id)
                distComp = dist
                if (str(val.deadline) == "EOD"):
                    distComp += 6
                if (id is not self.currentLocation and distComp < min): # 
                    min = dist
                    min_index = id
            
            if (min_index is not None):
                path.append([min_index, min])
                self.currentLocation = min_index
                Location.LocationMap.get(min_index).setVisited(True)
                timeSpent = timedelta(hours=(Truck.mph * dist))
                self.clock += timeSpent
                # print(timeSpent)
                packs = self.deliverPackages(Location.LocationMap.get(min_index))
                for pack in packs:
                    self.packages.remove(pack)

            else:
                dist = graph.DistanceToPoint(self.currentLocation, 0)
                path.append([0, dist])
                self.currentLocation = 0
                timeSpent = timedelta(hours=(Truck.mph * dist))
                self.clock += timeSpent
                # print(timeSpent)
                self.path = path
                return

        dist = graph.DistanceToPoint(self.currentLocation, 0)
        path.append([0, dist])
        self.currentLocation = 0
        self.clock += timedelta(hours=(Truck.mph * dist))
        self.path = path
    
    def printHeader(self):
        print("\n\n{0:3} {1:40} {2:20} {3:6} {4:10} {5:8} {6:12} {7:16} {8:16} {9:20} {10:16}".format(
            "ID",
            "Devliery Address",
            "City",
            "State",
            "Zip Code",
            "Weight",
            "Deadline",
            "Time Loaded",
            "Time Delivered",
            "Current Status",
            "Delivered By"
        ))

        


        
