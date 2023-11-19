# Joshua Buker
# Student ID # 011008778

from classes import *
from threading import Thread
import math

# Create Graph (Also creates Location maps) and the main Package Hashmap based on the provided CSV files.
g = Graph("WGUPS Distance Table.csv")
Package.loadCSV("WGUPS Package File.csv")

# Create three truck objects that will start at the times specified.
truck1 = Truck("Truck 1", "8:00:00")
truck2 = Truck("Truck 2", "9:05:00")
truck3 = Truck("Truck 3", "10:20:00")

#Create pre-determined sets of packages for the first two trucks to handle deadlines and special requirements
packageSetOne = [1,40,4,29,7,13,14,15,16,19,20,21,34,39,30,2]
packageSetTwo = [3,37,38,5,6,18,25,26,27,35,28,31,32,36,22]

# Replace the ID values with the acutal package object from the main Package Map
for i, val in enumerate(packageSetOne):
    packageSetOne[i] = Package.PackageMap.get(val)
for i, val in enumerate(packageSetTwo):
    packageSetTwo[i] = Package.PackageMap.get(val)

# Load the package set into the trucks
truck1.load(packageSetOne)
truck2.load(packageSetTwo)

#Generate a path based on the packages loaded into the truck and record the process for later viewing
truck1.generatePathForPackages(g)
truck2.generatePathForPackages(g)

#Since the third truck is leaving at 10:20, this address who's address wrong will be updated to be correct before the trucks departure
Package.PackageMap.get(9).address = "410 S State St"
Package.PackageMap.get(9).zipCode = "84111"

# Create and drive a path that will reach all remaining packages not yet delivered.
truck3.getRemainingLocations(g)


# Using the path saved on each truck, find the sum of all stops made to find the total mileage of each truck and overall total
sumOne = 0
sumTwo = 0
sumThree = 0
for node in truck1.path:sumOne += node[1]
for node in truck2.path:sumTwo += node[1]
for node in truck3.path:sumThree += node[1]
sumOne = round(sumOne, 2)
sumTwo = round(sumTwo, 2)
sumThree = round(sumThree, 2)
sumTotal = round(sumOne + sumTwo + sumThree, 2)


# ================================== Main menu Loop ============================================
menuLoop = True
while (menuLoop):
    #Print main menu text
    print("\n\n")
    print("1) View All Details")
    print("2) View Packages by Timeframe")
    print("3) View Packages by ID")
    print("4) View Total Mileage")
    print("5) Exit Program")

    #Get input for command choice
    choice = input("\nEnter a command's number to pick it: ")

    # Switch Case to run each command.
    match choice:
        case "1":
            truck1.printHeader()
            previousTruck = "Truck 1"
            for i in range(1,41):
                pack = Package.PackageMap.get(i)
                pack.print()

            print("\nMiles Driven By Truck 1: {}".format(sumOne))
            print("Miles Driven By Truck 2: {}".format(sumTwo))
            print("Miles Driven By Truck 3: {}".format(sumThree))
            print("Total Miles Driven By All Trucks: {}".format(sumTotal))
        case "2":
            try:
                start = input("\nEnter a time (24 Hour Format): ")
                start = (datetime.strptime(start, "%H:%M")).time()
                print("\n")
            except:
                print("Please ensure the time follows HH:MM format\n")
                continue

            for i in range(1,41):
                package = Package.PackageMap.get(i)
                
                if (start >= package.timeDelivered):
                    print("Package #{} was delivered to {} at {} by {}".format(package.id, package.address, package.timeDelivered, package.deliveredBy))
                elif (start < package.timeLoaded):
                    print("Package #{} is still at the Hub".format(package.id))
                elif (start < package.timeDelivered and start >= package.timeLoaded):
                    print("Package #{} was loaded at {} by {} and on route to {}".format(package.id, package.timeLoaded, package.deliveredBy, package.address))

        case "3":
            try:
                id = int(input("\nEnter a Package ID: "))
                package = Package.PackageMap.get(id)
            except:
                print("Please enter a numeric value for the ID.")

            if (package is not None):
                truck1.printHeader()
                package.print()
            else:
                print("package with ID {} does not exist.".format(id))
        case "4":
            print("\nMiles Driven By Truck 1: {}".format(sumOne))
            print("Miles Driven By Truck 2: {}".format(sumTwo))
            print("Miles Driven By Truck 3: {}".format(sumThree))
            print("Total Miles Driven By All Trucks: {}".format(sumTotal))
        case "5":
            exit()
        case default:
            print("That command is not recognized. Please use the provided numbers to choose the command")

            
