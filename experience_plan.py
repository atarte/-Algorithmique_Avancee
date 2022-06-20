from pulp import *
from copy import *

def Convert_to_complete(matrix, city_to_pass):
    new_matrix = deepcopy(matrix)
    for i in range(len(matrix)-1, -1, -1):
        if i not in city_to_pass:
            new_matrix.pop(i)
            for j in range(len(new_matrix)):
                new_matrix[j].pop(i)
    
    return new_matrix


def Borne(nb_vertex, tsp_matrix):
    StateMat = {}
    for i in range(nb_vertex):
        for j in range(nb_vertex):  # create a binary variable
            StateMat[i, j] = LpVariable('x{},{}'.format(i, j), cat='Binary')

    # probleme
    prob = LpProblem("Shortest_Delivery", LpMinimize)

    # fonction objective
    cost = lpSum([[tsp_matrix[n][m]*StateMat[n, m]
                 for m in range(nb_vertex)] for n in range(nb_vertex)])
    prob += cost

    # contrainte
    for n in range(nb_vertex):
        prob += lpSum([StateMat[n, m] for m in range(nb_vertex)]
                      ) == 1, "One place constraint "+str(n)

    cont2 = lpSum([StateMat[m, m]
                  for m in range(nb_vertex)]) == 0, "No loop constraint"
    prob += cont2

    prob.solve()
    return value(prob.objective) if (LpStatus[prob.status] == "Optimal") else None
