# Created using https://www.youtube.com/watch?v=9HFbhPscPU0&ab_channel=OggiAI-ArtificialIntelligenceToday
#merged with https://srm--c.vf.force.com/apex/coursearticle?Id=kA03x000000e1fuCAA
class HashMap:
    size = 10

    def __init__(self, initialSize):
        self.size = initialSize
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
                print(str(item))

inventory = HashMap(10)

inventory.add(0, "Package 0")
inventory.add(1, "Package 1")
inventory.add(2, "Package 2")
inventory.add(3, "Package 3")
inventory.add(4, "Package 4")
inventory.add(5, "Package 5")
inventory.add(6, "Package 6")
inventory.add(7, "Package 7")
inventory.add(8, "Package 8")
inventory.add(9, "Package 9")

inventory.print()
print(inventory.get(4))
