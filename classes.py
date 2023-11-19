from enum import Enum
from datetime import *
import csv

# ============================== STATUS ENUM =================================

# Basic enum for minimising status options to keep everything organized
class Status(Enum):
    HUB = "at the Hub"
    TRANSIT = "in transit"
    DELIVERED = "delivered"


# ============================= HASH TABLE CLASS =============================

# Basic Hashmap created following Joe James's YouTube tutorial found here https://www.youtube.com/watch?v=9HFbhPscPU0&ab_channel=OggiAI-ArtificialIntelligenceToday, mixed with pieces I prefered from
# https://srm--c.vf.force.com/apex/coursearticle?Id=kA03x000000e1fuCAA
class HashMap:
    # Constructor method that sets the default size of the hashmap to 20 and populates it with empty arrays.
    def __init__(self):
        self.size = 20
        self.map = []
        for i in range(self.size):
            self.map.append([])
    
    # Add method to insert key/value pairs into hashmap. Also serves as an update method when passed a pre-existing key.
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
    
    # Returns the value associated with the key provided.
    def get(self, key):
        kh = hash(key) % self.size
        if (self.map[kh] is not None):
            for pair in self.map[kh]:
                if pair[0] == key:
                    return pair[1]
        return None
    
    # Deletes a key/value pair based on the provided key
    def delete(self, key):
        kh = hash(key) % self.size

        if (self.map[kh] is None):
            return False
        for i in range (0, len(self.map[kh])):
            if self.map[kh][i][0] == key:
                self.map[kh].pop(i)
                return True
    
    # Prints the items in the hashmap while ignoring the empty slots
    def print(self):
        for item in self.map:
            if item is not None:
                if item:
                    print(str(item))

# ============================== GRAPH CLASS =================================
# Basic graph creation technique and Dijkstra's Algorthm were found and modifed from https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/#
class Graph():
    #Creates a graph based on a provided csv file path
    def __init__(self, file):
        graphPair = self.loadCSV(file)

        self.graph = graphPair[0]
        self.V = graphPair[1]
        self.visited = [None]*self.V

    # Creates graph from csv along with populating the Location maps. I know that object shouldn't be too interconnected since it takes away modulatity, but
    # since this function was already reading and looping through the file, I figured it would save time to just do it here.
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
                    # Turn spelled out directions to their letters to better normalize the data
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
            
        # The provided csv only contains half of the matrix needed for this graph to work, so this mirrors the values to the other side
        graphArray[0][0] = float(graphArray[0][0])
        for i, arr in enumerate(graphArray):
            for j in range(i+1):
                graphArray[i][j] = float(graphArray[i][j])
                graphArray[j][i] = graphArray[i][j]
        graphArray[length-1][length-1] = float(graphArray[length-1][length-1])

        return [graphArray, length]
    
    # Finds the minimum distance between vertices
    def minDistance(self, dist, sptSet):
        min = 1e7
 
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
    
    # Dijkstra's algorithm. From a source point, get the shortest distance path to each of the other vertices in the graph.
    # After I had already finished the program 90+ percent, I realized that due to the fact the matrix is fully connected, this algorithm is not needed at all, and if anything
    # only slows it down. However I felt like I should keep it so that I can get experience with it and so if this ever gets used with data that isnt fully connected, it will support it.
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
    
    # Addition to Dijkstra's where grabs the distance between two points using the distance array created in the 'DistanceToAllPoints' method
    def DistanceToPoint(self, src, end):
        return self.DistanceToAllPoints(src)[end]
    
    # My attempt at a Nearest Neighbor algorithm using a modified approach from the dijskra's 'minDistance' method. 
    # Given a location index, it will loop to each connected node and check if it is vistited alongside checking if it is the smallest distance. 
    # Unless both requirements are met, it will just skip and go to the next index to check.
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
    
    # This was an early prototype of my Truck's 'generatePathForPackage' method. The difference with this is it is a true nearest neighbor algorithm and will find an entire path
    # start to finish. 
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
#Package class to store all the data each package requires. 
class Package():
    PackageMap = HashMap()

    # Constructor Method
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

    # Using the Package file csv, this method loads each package and saves it to the class variable 'PackageMap' which all other truck objects will use. 
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
                    # Turn spelled out directions to their letters to better normalize the data
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

    # A do it all status and time method. Depending on what status is being set, it will update the required variable to store the time for each event type
    def setStatus(self, status, currentTime, truck): 
        self.status = status
        self.deliveredBy = truck.label

        match status:
            case Status.DELIVERED:
                self.timeDelivered = currentTime.time()
            case Status.TRANSIT:
                self.timeLoaded = currentTime.time()

    # Prints the package data in a table like structure to make it easier to read for the user. Used in conjunction with the truck's 'printHeader' method to add the table headers
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
#Location object used to store an address and the visited status. Used for nearest neighbor algorithm and for choosing which packages need to be delivered at which stops
class Location():
    LocationMap = HashMap()
    LocationToIDMap = HashMap()

    # Constructor method
    def __init__(self, address, visited):
        self.address = address
        self.visited = visited
    
    # Changes the objects visited boolean accordingly
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

    # Loads the provided path into an internal array for later use
    def setPath(self, path):
        self.path = path
    
    # Loads a set of packages into the truck to be delivered
    def load(self, packages):
        self.packages = packages

        for package in self.packages:
            package.setStatus(Status.TRANSIT, self.clock, self)

    # Given a location, it will search the trucks packages for the address and sets their status to delivered. Optionally you can uncomment the print statement to have a
    # cronological timeline of each package being delivered for each truck.
    def deliverPackages(self, location):
        deliveredPackages = []

        for idx, package in enumerate(self.packages):
            if (package.address == location.address):
                package.setStatus(Status.DELIVERED, self.clock, self)
                # package.print()
                deliveredPackages.append(package)

        return deliveredPackages
    
    # Using the interal array of package objects, this function will find the locations needed for them and then deploy the nearest neighbor algorithm in order to reach each of them in
    # the shortest distance. However due to deadlines, I have applied a +6 mile offset to non-deadline stops. This will artifically make the algorithm favor going towards deadline targets.
    def generatePathForPackages(self, graph):
        locations = []
        path = []

        # self.printHeader()

        # Main delivery loop
        for i in range (0, len(self.packages)):
            min = 1e7
            min_index = None

            # Find the location with the shortest distance from the current location of the truck
            for idx, val in enumerate(self.packages):
                id = Location.LocationToIDMap.get(val.address)
                dist = graph.DistanceToPoint(self.currentLocation, id)
                distComp = dist
                # If the package does not have a deadline attached to it, artificially add 6 miles to the distance to make it a less desirable location to travel.
                # This will make deadline packages a higher priority
                if (str(val.deadline) == "EOD"):
                    distComp += 6
                if (id is not self.currentLocation and distComp < min and Location.LocationMap.get(id).visited == False): 
                    min = dist
                    min_index = id
            
            # If a location is found, add the location to the path including the distance to said location. Then set current location, set location to visted, add the amount of time it took
            # based on distance * the MPH of the truck (18mph) to the internal clock of the truck. 
            if (min_index is not None):
                path.append([min_index, min])
                self.currentLocation = min_index
                Location.LocationMap.get(min_index).setVisited(True)
                timeSpent = timedelta(hours=(Truck.mph * dist))
                self.clock += timeSpent
                # print(timeSpent)
                self.deliverPackages(Location.LocationMap.get(min_index))
                
            # If a location is not found, that means it failed or all stops have been made. Therefore run Dijsktra's to find a path back to the main hub.
            else:
                dist = graph.DistanceToPoint(self.currentLocation, 0)
                path.append([0, dist])
                self.currentLocation = 0
                timeSpent = timedelta(hours=(Truck.mph * dist))
                self.clock += timeSpent
                # print(timeSpent)
                self.path = path
                return

        # If the previous go home else statement doesn't get triggered, this one will ensure that the truck returns to the Hub regardless of what happens.
        dist = graph.DistanceToPoint(self.currentLocation, 0)
        path.append([0, dist])
        self.currentLocation = 0
        self.clock += timedelta(hours=(Truck.mph * dist))
        self.path = path
        
    # This is a modified pathGenerator that doesn't require a package set to be loaded. It determines which packages have not been delivered and will go to each location regardless
    # of their visited status while also using the nearest neighbor algorithm for traversal and dijsktra's for returning to the hub.
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
    
    # Print a table style header to pair with the delivery print statements.
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

        


        
