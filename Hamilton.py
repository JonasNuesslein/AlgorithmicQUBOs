import math
import utils




class Hamilton:

    def __init__(self, V, E, edges):
        self.V = V
        self.E = E
        self.edges = edges
        self.Q = {}
        self.z = math.ceil(math.log2(self.V+1))
        self.zValues = [2 ** i for i in range(self.z)]

    # new values are added to the QUBO-Matrix Q via this monitor
    def add(self, x, y, value):
        if x > y:
            x,y = y,x
        if (x,y) in self.Q.keys():
            self.Q[(x,y)] += value
        else:
            self.Q[(x,y)] = value

    # this function creates the QUBO-Matrix Q
    # Explanations can be found in the paper
    def fillQ(self):
        for edgeNr1, (a, b) in enumerate(self.edges):
            if b == 0:
                for z1 in range(self.z):
                    self.add(edgeNr1 * self.z + z1, edgeNr1 * self.z + z1, -2 * self.zValues[z1] * (self.V + 1))
                    for z2 in range(self.z):
                        self.add(edgeNr1 * self.z + z1, edgeNr1 * self.z + z2, 2 * self.zValues[z1] * self.zValues[z2])
            else:
                for z1 in range(self.z):
                    for z2 in range(self.z):
                        self.add(edgeNr1 * self.z + z1, edgeNr1 * self.z + z2, 2 * self.zValues[z1] * self.zValues[z2])
            for edgeNr2, (c, d) in enumerate(self.edges):
                if edgeNr2 >= edgeNr1:
                    continue
                if (a == c or b == d) and not (a == c and b == d):
                    for z1 in range(self.z):
                        for z2 in range(self.z):
                            self.add(edgeNr1 * self.z + z1, edgeNr2 * self.z + z2, 2 * self.V * self.V)
                elif (b == c and b != 0) or (a == d and a != 0):
                    for z1 in range(self.z):
                        for z2 in range(self.z):
                            self.add(edgeNr1 * self.z + z1, edgeNr2 * self.z + z2, -2 * self.zValues[z1] * self.zValues[z2])

    # this function starts creating Q, solving it and interpreting the solution
    # (e.g. deciding whether there is a hamilton path in the graph or not)
    def solve(self):
        self.fillQ()
        answer = utils.solve_with_qbsolv(self.Q)
        value = utils.getValue(self.Q, answer)
        #print("Value: ", value, "[", -self.V * (self.V + 1), "]")
        print("Size of Q: ", self.z*self.E)
        path = [-1] * (self.V+1)
        path[0] = 0
        path[self.V] = 0
        for edgeNr, (a, b) in enumerate(self.edges):
            pos = 0
            for z1 in range(self.z):
                pos += self.zValues[z1] * answer[edgeNr * self.z + z1]
            if pos != 0:
                path[pos] = b
        if value > -self.V * (self.V + 1):
            return False
        else:
            print("The hamilton path is: ", path)
            return True




V, E = 7, 25
edges = utils.createRandomGraph(V, E)
print(edges)
print("There is a hamilton path: ", Hamilton(V, E, edges).solve())

