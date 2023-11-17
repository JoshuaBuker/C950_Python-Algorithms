from classes import *
from threading import Thread

g = Graph("WGUPS Distance Table.csv")
Package.loadCSV("WGUPS Package File.csv")

truck1 = Truck("Truck 1", "8:00:00")
truck2 = Truck("Truck 2", "9:05:00")
truck3 = Truck("Truck 3", "8:00:00")

packageSetOne = [1,40,4,29,7,13,14,15,16,19,20,21,34,39,33,2]
packageSetTwo = [3,37,38,5,6,18,25,26,27,35,28,31,32,36,22,23]
packageSetThree = [30,9,8,10,11,12,17,24]

for i, val in enumerate(packageSetOne):
    packageSetOne[i] = Package.PackageMap.get(val)
for i, val in enumerate(packageSetTwo):
    packageSetTwo[i] = Package.PackageMap.get(val)
for i, val in enumerate(packageSetThree):
    packageSetThree[i] = Package.PackageMap.get(val)


truck1.load(packageSetOne)
truck2.load(packageSetTwo)
truck3.load(packageSetTwo)

print("Truck 1:")
truck1.generatePathForPackages(g)
print("Truck 2:")
truck2.generatePathForPackages(g)

if (truck1.clock > truck2.clock):
    truck3.clock = truck2.clock
else:
    truck3.clock = truck1.clock

print("Truck 3:")
truck3.getRemainingLocations(g)

sum = 0
for node in truck1.path:
    sum += node[1]
for node in truck2.path:
    sum += node[1]
for node in truck3.path:
    sum += node[1]

print(sum)
