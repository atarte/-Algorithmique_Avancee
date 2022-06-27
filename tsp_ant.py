import sys
import random as rand
from functools import lru_cache
from copy import *


def Get_Next_City(matrix, pheromone_matrix, path, cities_to_pass, current_city, alpha, beta):
    '''
    Returns a city where the random proportional transition rule 
    '''
    denominator_sum = 0
    probabilities_list = []
    available_cities = tuple(city for city in cities_to_pass if city not in path)

    for city in available_cities:
        denominator_sum += pow(pheromone_matrix[current_city]
                               [city], alpha) * pow(1 / matrix[current_city][city], beta)


    for city in available_cities:

        probabilities_list.append(
            (pow(pheromone_matrix[current_city][city], alpha)
             * pow(1 / matrix[current_city][city], beta)) / denominator_sum
        )

    return rand.choices(available_cities, weights=probabilities_list, k=1)[0]


def Update_Pheromone(pheromone_matrix, path, path_lenght, evaporation_factor, pheromone_spread):
    '''
    Returns the pheromone matrix after updating the pheromone trails
    '''
    pheromone_to_apply = pheromone_spread / path_lenght

    for i in range(len(pheromone_matrix)):
        for j in range(len(pheromone_matrix)):
            pheromone_matrix[i][j] = pheromone_matrix[i][j] * \
                evaporation_factor if pheromone_matrix[i][j] <= 1.0e-250 else 1.0e-10

    for i in range(len(path) - 1):
        pheromone_matrix[path[i]][path[i + 1]] += pheromone_to_apply
        pheromone_matrix[path[i + 1]][path[i]] += pheromone_to_apply

    return pheromone_matrix


@lru_cache(maxsize=512)
def Get_Path_Lenght(graph, path):
    '''
    Returns the length of a path
    '''
    path_lenght = 0

    for i in range(len(path) - 1):
        path_lenght += graph[path[i]][path[i + 1]]

    return path_lenght


def Ant_Tsp(graph, cities_to_pass, nb_iteration = 50, nb_ant = 25, alpha=0.5, beta=5.0, evaporation_factor=0.25, pheromone_spread=0.9):
    '''
    Returns the optimal path through the verteces <cities_to_pass> of the graph <graph> with the algoritm "Ant Colony Optimization"
    '''
    best_path = ()
    shortest_path = sys.maxsize
    pheromone = tuple([1 for _ in graph] for _ in graph)

    for _ in range(nb_iteration):
        pheromone_matrix = deepcopy(pheromone)
        for _ in range(nb_ant):

            path = []
            current_city = rand.choice(cities_to_pass)
            path.append(current_city)

            for _ in range(len(cities_to_pass) - 1):

                next_city = Get_Next_City(graph, pheromone_matrix, path, cities_to_pass, current_city, alpha, beta)
                path.append(next_city)
                current_city = next_city

            path.append(path[0])
            path = tuple(path)

            path_lenght = Get_Path_Lenght(graph, path)
            if path_lenght < shortest_path:
                best_path = path
                shortest_path = path_lenght

            pheromone_matrix = Update_Pheromone(pheromone_matrix, path, path_lenght, evaporation_factor, pheromone_spread)

    return best_path, shortest_path