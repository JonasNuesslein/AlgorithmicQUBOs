import utils
import math
import numpy as np
import copy



class kSAT:

    def __init__(self, formula, V):
        # sort the formula (i.e. all negative literals are at the back of the clause)
        self.formula = [sorted(c, reverse=True) for c in formula]
        self.V = V
        self.Q = {}

    # new values are added to the QUBO-Matrix Q via this monitor
    def add(self, x, y, value):
        x = abs(x) - 1
        y = abs(y) - 1
        if x > y:
            x,y = y,x
        if (x,y) in self.Q.keys():
            self.Q[(x,y)] += value
        else:
            self.Q[(x,y)] = value

    # this function creates the QUBO-Matrix Q
    # Explanations can be found in the paper
    def fillQ(self):
        offset = self.V + 1 # offset points to the next free space
        formula = copy.deepcopy(self.formula) # copy in order to keep self.formula unchanged
        for c in formula:
            if len(c) == 2:
                if list(np.sign(c)) == [1,1]:
                    self.add(abs(c[0]), abs(c[0]), -1)
                    self.add(abs(c[1]), abs(c[1]), -1)
                    self.add(abs(c[0]), abs(c[1]), 1)
                elif list(np.sign(c)) == [1,-1]:
                    self.add(c[0], c[1], -1)
                    self.add(c[1], c[1], 1)
                else:
                    self.add(c[0], c[1], 1)
            elif len(c) == 3:
                if list(np.sign(c)) == [1,1,1]:
                    self.add(c[0], c[1], 2)
                    self.add(c[0], offset, -2)
                    self.add(c[1], offset, -2)
                    self.add(c[2], c[2], -1)
                    self.add(c[2], offset, 1)
                    self.add(offset, offset, 1)
                elif list(np.sign(c)) == [1,1,-1]:
                    self.add(c[0], c[1], 2)
                    self.add(c[0], offset, -2)
                    self.add(c[1], offset, -2)
                    self.add(c[2], c[2], 1)
                    self.add(c[2], offset, -1)
                    self.add(offset, offset, 2)
                elif list(np.sign(c)) == [1,-1,-1]:
                    self.add(c[0], c[0], 2)
                    self.add(c[0], c[1], -2)
                    self.add(c[0], offset, -2)
                    self.add(c[1], offset, 2)
                    self.add(c[2], c[2], 1)
                    self.add(c[2], offset, -1)
                else:
                    self.add(c[0], c[0], -1)
                    self.add(c[0], c[1], 1)
                    self.add(c[0], c[2], 1)
                    self.add(c[0], offset, 1)
                    self.add(c[1], c[1], -1)
                    self.add(c[1], c[2], 1)
                    self.add(c[1], offset, 1)
                    self.add(c[2], c[2], -1)
                    self.add(c[2], offset, 1)
                    self.add(offset, offset, -1)
                offset += 1
            else:
                h = math.ceil(math.log2(len(c)+1))
                var = [abs(l) for l in c]
                var.extend([offset+i for i in range(h)])
                val = [np.sign(l) for l in c]
                val.extend([-(2**i) for i in range(h)])
                for l1 in range(len(var)):
                    self.add(var[l1], var[l1], 2*self.n(c)*val[l1])
                    for l2 in range(len(var)):
                        self.add(var[l1], var[l2], val[l1]*val[l2])
                formula.append([offset+i for i in range(h)])
                offset += h

        print("Size of Q: ", offset)

    # returns how many literals in the clause c are negations
    def n(self, c):
        return len([1 for l in c if l < 0])

    # this function starts creating Q, solving it and interpreting the solution
    # (e.g. deciding whether the formula is satisfiable or not)
    def solve(self):
        self.fillQ()
        answer = utils.solve_with_qbsolv(self.Q)
        assignment = [answer[i] for i in range(self.V)]
        print("Assignment: ", assignment)
        return utils.check_solution(self.formula, assignment)




V = 7
formula = utils.download_formula(V, num_clauses=20, k=3)
print(formula)
print("Satisfiable: ", kSAT(formula, V).solve())
