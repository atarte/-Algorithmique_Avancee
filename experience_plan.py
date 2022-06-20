import tsp_ant as tsp_ant

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


def Limit_Ant(graph, cities_to_pass):
    '''
    ok
    '''

    for interation in range(100, 1100, 100):
        for ant in range(10, 210, 10):
            for alpha in range(0.1, 5.0, 0.1):
                for beta in range(0.1, 5.0, 0.1):
                    for evaporation_factor in range(0.1, 1.0, 0.1):
                        for pheromone_spread in range(0.5, 5.0, 0.5):
                            _ = tsp_ant.Ant_Tsp(graph, cities_to_pass, nb_iteration=interation, nb_ant=ant, alpha=alpha, beta=beta, evaporation_factor=evaporation_factor, pheromone_spread=pheromone_spread)
                            
