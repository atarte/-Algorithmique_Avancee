import sys
import random as rand

def Get_Next_City(matrix, pheromone_matrix, path, cities_to_pass, current_city):
    '''
    Returns a city where the random proportional transition rule 
    '''

    alpha = 1.0
    beta = 2.0

    available_cities = [city for city in cities_to_pass if city not in path]

    # if len(available_cities) == 0:
    #     return

    denominator_sum = 0

    for city in available_cities:
        intensity = pheromone_matrix[current_city][city]
        visibility = 1 / matrix[current_city][city]
        denominator_sum += pow(intensity, alpha) * pow(visibility, beta)

    probabilities_list = []

    for city in available_cities:
        intensity = pheromone_matrix[current_city][city]
        visibility = 1 / matrix[current_city][city]
        probability = (pow(intensity, alpha) * pow(visibility, beta)) / denominator_sum
        probabilities_list.append([
            city,
            probability
        ])

    probabilities_list_sorted = sorted(
        probabilities_list, key=lambda x: x[1], reverse=True)

    return probabilities_list_sorted[0][0]


def Update_Pheromone(pheromone_matrix, path, path_lenght):
    '''
    Returns the pheromone matrix after updating the pheromone trails
    '''
    evaporation_factor = 0.3 # 30% des phéromone sévapore

    for i in range(len(pheromone_matrix)):
        for j in range(len(pheromone_matrix)):
            pheromone_matrix[i][j] *= (1 - evaporation_factor)
    pheromone_spread = 1.0
    pheromone_to_apply = pheromone_spread / path_lenght

    for i in range(len(path) - 1):
        pheromone_matrix[path[i]][path[i + 1]] = pheromone_to_apply
        pheromone_matrix[path[i + 1]][path[i]] = pheromone_to_apply

    return pheromone_matrix


def Get_Path_Lenght(graph, path):
    '''
    Returns the length of a path
    '''
    path_lenght = 0

    for i in range(len(path) - 1):
        path_lenght += graph[path[i]][path[i + 1]]

    return path_lenght


def Ant_Tsp(graph, cities_to_pass, nb_iteration = 100, nb_ant = 10):
    '''
    Returns the optimal path through the verteces <cities_to_pass> of the graph <graph> with the algoritm "Ant Colony Optimization"
    '''
    # pheromone_matrix = [
    #     [1 if column != 0 else 0 for column in range(row)] for row in range(graph)]
    pheromone_matrix = [[1 for _ in graph] for _ in graph]
    for i in range(len(pheromone_matrix)):
        pheromone_matrix[i][i] = 0

    best_path = []
    path = []
    shortest_path = sys.maxsize

    for i in range(nb_iteration):
        # print('interation : ', i)
        for ant in range(nb_ant):
            # print('fourmis : ', ant)

            path = []
            current_city = rand.choice(cities_to_pass)
            path.append(current_city)

            for _ in range(len(cities_to_pass) - 1):

                next_city = Get_Next_City(graph, pheromone_matrix, path, cities_to_pass, current_city)
                path.append(next_city)
                current_city = next_city

            path.append(path[0])

            path_lenght = Get_Path_Lenght(graph, path)
            if path_lenght < shortest_path:
                best_path = path

            pheromone_matrix = Update_Pheromone(pheromone_matrix, path, path_lenght)

    return best_path


if __name__ == '__main__':
    print('cool')