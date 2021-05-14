import requests
from dwave_qbsolv import QBSolv
import random



# this function downloads a random k-SAT formula
def download_formula(num_vars, num_clauses, k):

    data = {
        "type": "random_ksat",
        "lits_per_clause": k,
        "numvariables": num_vars,
        "numclauses": num_clauses,
        "generate": "Generate"
    }

    answer = requests.post("https://toughsat.appspot.com/generate", data)

    if answer.status_code == 200:
        formula = []
        for line_index, line in enumerate(answer.text.split("\n")):
            if line_index < 2 or line == "":
                continue
            else:
                clause_string = line.split(" ")
                formula.append([int(clause_string[var]) for var in range(k)])
        return formula
    else:
        return None



# this function solves a given QUBO-Matrix Q with Qbsolv
def solve_with_qbsolv(Q):
    response = QBSolv().sample_qubo(Q, num_repeats=1000)
    return response.samples()[0]



# this function calculates the value of a solution for a given QUBO-Matrix Q
def getValue(Q, solution):
    ones = [x for x in solution.keys() if solution[x] == 1]
    value = 0
    for x in ones:
        for y in ones:
            if (x,y) in Q.keys():
                value += Q[(x,y)]
    return value



# this function prints the first n row/columns of a QUBO-Matrix Q
def printQUBO(Q, n):
    for row in range(n):
        for column in range(n):
            if row > column:
                print("      ", end = '')
                continue
            printing = ""
            if (row,column) in Q.keys() and Q[(row,column)] != 0:
                printing = str(Q[(row,column)])
            printing += "_____"
            printing = printing[:5]
            printing += " "
            print(printing, end = '')
        print("")



# this function checks, whether a given assignment satisfies a given SAT-formula
def check_solution(formula, assignment):
    for c in formula:
        sat = False
        for l in c:
            if l < 0 and assignment[abs(l)-1] == 0:
                sat = True
            elif l > 0 and assignment[abs(l)-1] == 1:
                sat = True
        if not sat:
            print(c) # print the clause which is not satisfied under the assignment
            return False
    return True



# this function creates a random graph with V nodes and E edges.
# It returns a list called edges with tuples (a,b) representing an directed edge from node a to b
def createRandomGraph(V, E):
    if E > 2*V*(V-1):
        print("ERROR. Too many edges wanted!")
        return None
    edges = []
    while len(edges) < E:
        a = random.choice(range(V))
        b = random.choice(range(V))
        if a != b and (a,b) not in edges:
            edges.append((a,b))
    return edges
