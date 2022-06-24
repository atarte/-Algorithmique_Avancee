import sys
# import random as rand
from functools import lru_cache


def Get_Next_City(matrix, pheromone_matrix, path, cities_to_pass, current_city, alpha, beta):
    '''
    Returns a city where the random proportional transition rule 
    '''
    denominator_sum = 0
    probabilities_list = []
    available_cities = tuple(city for city in cities_to_pass if city not in path)

    for city in available_cities:
        # intensity = pheromone_matrix[current_city][city]
        # visibility = 1 / matrix[current_city][city]
        # denominator_sum += pow(intensity, alpha) * pow(visibility, beta)
        denominator_sum += pow(pheromone_matrix[current_city]
                               [city], alpha) * pow(1 / matrix[current_city][city], beta)


    for city in available_cities:
        # intensity = pheromone_matrix[current_city][city]
        # visibility = 1 / matrix[current_city][city]
        # probability = (pow(intensity, alpha) * pow(visibility, beta)) / denominator_sum
        # probabilities_list.append([
        #     city,
        #     probability
        # ])
        probabilities_list.append([
            city,
            (pow(pheromone_matrix[current_city][city], alpha)
             * pow(1 / matrix[current_city][city], beta)) / denominator_sum
        ])


    probabilities_list_sorted = sorted(
        probabilities_list, key=lambda x: x[1], reverse=True)

    return probabilities_list_sorted[0][0]


def Update_Pheromone(pheromone_matrix, path, path_lenght, evaporation_factor, pheromone_spread):
    '''
    Returns the pheromone matrix after updating the pheromone trails
    '''
    pheromone_to_apply = pheromone_spread / path_lenght

    for i in range(len(pheromone_matrix)):
        for j in range(len(pheromone_matrix)):
            # pheromone_matrix[i][j] *= (1 - evaporation_factor)
            # if pheromone_matrix[i][j] <= 1.0e-250:
            #     pheromone_matrix[i][j] = 1.0e-10
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


@lru_cache(maxsize=512)
def Ant_Tsp(graph, cities_to_pass, nb_iteration = 100, nb_ant = 10, alpha=1.0, beta=2.0, evaporation_factor=0.3, pheromone_spread=1.0):
    '''
    Returns the optimal path through the verteces <cities_to_pass> of the graph <graph> with the algoritm "Ant Colony Optimization"
    '''
    best_path = ()
    shortest_path = sys.maxsize

    for _ in range(nb_iteration):
        pheromone_matrix = tuple ([1 for _ in graph] for _ in graph)

        for _ in range(nb_ant):

            path = []
            # current_city = rand.choice(cities_to_pass)
            current_city = cities_to_pass[0]
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


# if __name__ == '__main__':