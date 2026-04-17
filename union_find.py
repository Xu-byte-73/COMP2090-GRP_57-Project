from abc import ABC, abstractmethod

class UnionFindInterface(ABC): #union-find ADT
    @abstractmethod
    def makeSet(self, x): #create a new set containing the element itself
        ...

    @abstractmethod
    def find(self, x): #find the root
        ...

    @abstractmethod
    def union(self, x, y): #conbine set of x and set of y if disjoint
        ...

class UnionFind(UnionFindInterface):
    def __init__(self, n):
        self.parent = list(range(n)) #implicit makeset
        self.rank = [0] * n #initialize rank for elements

    def makeSet(self, id):
        self.parent[id] = id #set parent of an element to itself
        self.rank[id] = 0
        

    def find(self, id):
        if self.parent[id] != id:
            self.parent[id] = self.find(self.parent[id]) #path compression

        return self.parent[id]
    
    def union(self, id_1, id_2):
        id_root1, id_root2 = self.find(id_1), self.find(id_2)
        if self.find(id_1) == self.find(id_2): #no behabiour if in the same set
            return False
        
        if self.rank[id_root1] < self.rank[id_root2]: #union by rank
            self.parent[id_root1] = id_root2
        elif self.rank[id_1] > self.rank[id_2]:
            self.parent[id_root2] = id_root1
        else:
            self.parent[id_root2] = id_root1 #increment by 1 if same rank
            self.rank[id_root1] += 1

        return True