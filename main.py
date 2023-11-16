from classes import *

g = Graph("WGUPS Distance Table.csv")

# for i in range(27): print(str(i) + ":  " + Location.LocationMap.get(i).address)

dist = g.DistanceToAllPoints(0)

# for i in range(len(dist)):
#     print("{0}: {1:40} {2}".format(i, Location.LocationMap.get(i).address, dist[i]))

distance = 0
currentLocation = 0
Location.LocationMap.get(currentLocation).setVisited(True)
while (True):
    coords = g.NearestPointFrom(currentLocation, Location.LocationMap)

    if (coords is not False):
        print("{} :-: {}".format(Location.LocationMap.get(coords[0]).address, coords))
        Location.LocationMap.get(coords[0]).setVisited(True)
        currentLocation = coords[0]
        distance += coords[1]
    else:
        homeDist = g.DistanceToPoint(currentLocation, 0)
        print("[{0}, {1}]".format(0, homeDist))
        distance += homeDist
        break

print(distance)

print(g.DistanceToPoint(2, 25))