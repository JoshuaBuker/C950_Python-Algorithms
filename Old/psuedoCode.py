# Main loop for the program to run
function MainProgramLoop:
    truck1.NearestNeighborPathMaker(for location "4300 S 1300 E" and 16 Packages)
    truck2.NearestNeighborPathMaker(for location "177 W Price Ave" and 16 Packages)

# Get a certain number of locations from starting location using Nearest Neighbor Algorithm and the required package
function NearestNeighborPathMaker(Starting Location, Number of Packages):
    PathArray Equals [Empty Array]
    PackagesArray Equals [Empty Array]

    Current Location Equals Starting Location

    LOOP FOR (Number of Packages) {
        Find closest location from current location
        Add Closest Location to PathArray
        Add PackagesHashTable.search(Location) to PackagesArray
        CurrentLocation Equals Closest Location
    }

    truck.load(PackagesArray)
    truck.setPath(PathArray)
    
    Truck start Diving

#Go to each location the path describes. Once all locations are visited, return to hub
function Driving():
    WHILE Packages are left in truck {
        Truck Set Current Location and Distance
        Truck Deliver Package 
        Truck Drive to Next Location
    }

    Return To Hub Using Dijksta (Current Location, "Western Governors University")
