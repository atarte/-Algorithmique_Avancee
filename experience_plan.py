import tsp_ant as tsp_ant

from pulp import *
from copy import *
import numpy as np
import progressbar as pb

def Convert_to_complete(matrix, city_to_pass):
    new_matrix = deepcopy(matrix)
    new_matrix = list(new_matrix)
    for i in range(len(matrix)-1, -1, -1):
        new_matrix[i] = list(new_matrix[i])

    for i in range(len(matrix)-1, -1, -1):
        if i not in city_to_pass:
            new_matrix.pop(i)
            for j in range(len(new_matrix)):
                new_matrix[j].pop(i)
    
    return new_matrix


def Borne(nb_vertex, tsp_matrix):
    StateMat = {}
    OrderList = {}
    for i in range(nb_vertex):
        for j in range(nb_vertex):  # create a binary variable
            StateMat[i, j] = LpVariable('x{},{}'.format(
                i, j), lowBound=0, upBound=1, cat=const.LpBinary)

    for i in range(nb_vertex):  # create a binary variable
        OrderList[i] = LpVariable('u{}'.format(
            i), lowBound=1, upBound=nb_vertex, cat=const.LpInteger)

    # probleme
    prob = LpProblem("Shortest_Delivery", LpMinimize)

    # fonction objective
    cost = lpSum([[tsp_matrix[n][m]*StateMat[n, m]
                 for m in range(nb_vertex)] for n in range(nb_vertex)])
    prob += cost

    # contrainte
    for n in range(nb_vertex):
        prob += lpSum([StateMat[n, m] for m in range(nb_vertex)]
                      ) == 1, "All entered constraint "+str(n)
        prob += lpSum([StateMat[m, n] for m in range(nb_vertex)]
                      ) == 1, "All exited constraint "+str(n)

    for i in range(nb_vertex):
        for j in range(nb_vertex):
            if i != j and (i != 0 and j != 0):
                prob += OrderList[i] - OrderList[j] <= nb_vertex * \
                    (1 - StateMat[i, j]) - 1

    cont2 = lpSum([StateMat[m, m]
                  for m in range(nb_vertex)]) == 0, "No loop constraint"
    prob += cont2

    prob.solve()
    return prob.objective.value() if (LpStatus[prob.status] == "Optimal") else None


def Limit_Ant(graph, cities_to_pass, nb_test):
    '''
    ok
    '''
    widgets = [' ['
               , pb.Timer(),
            '] ',
            pb.Bar('*'),' (',
            pb.ETA(), ') ',
            ]
    
    nb_steps_bar = nb_test

    VarIteration = range(100, 1100, 500)
    nb_steps_bar *= len(VarIteration)

    VarAnt = range(10, 210, 30)
    nb_steps_bar *= len(VarAnt)

    VarAlpha = range(1, 50, 10)
    nb_steps_bar *= len(VarAlpha)

    VarBeta = range(1, 50,10)
    nb_steps_bar *= len(VarBeta)

    VarEvap = range(1, 10, 3)
    nb_steps_bar *= len(VarEvap)

    VarPheromone = range(5, 50, 10)
    nb_steps_bar *= len(VarPheromone)

    print(nb_steps_bar)

    Textbar = pb.ProgressBar(maxval=nb_steps_bar, widgets=widgets)
    Textbar.start()

    value = 0

    complete_matrix = Convert_to_complete(graph, cities_to_pass)
    limit = Borne(len(complete_matrix), complete_matrix)

    list_average = []

    for interation in VarIteration:
        for ant in VarAnt:
            for alpha in VarAlpha:
                for beta in VarBeta:
                    for evaporation_factor in VarEvap:
                        for pheromone_spread in VarPheromone:
                            current_values = []

                            for _ in range(nb_test):
                                _, path_lenght = tsp_ant.Ant_Tsp(graph, cities_to_pass, nb_iteration=interation, nb_ant=ant, alpha=alpha/10, beta=beta/10, evaporation_factor=evaporation_factor/10, pheromone_spread=pheromone_spread/10)
                                
                                current_values.append((path_lenght / limit) * 100)
                                value += 1
                                Textbar.update(value)
                                
                            list_average.append(np.mean(current_values))

    Textbar.finish()
    
    total_average = np.mean(list_average)
    total_derivation = np.nanstd(list_average)


    print(total_average + total_derivation)
    print(total_average)
    print(total_average - total_derivation)
