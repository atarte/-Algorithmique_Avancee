import numpy as np
from numpy.linalg import matrix_power
import random as rand


def Fix_Matrix_Not_Connected(matrix):
    '''
    Returns a connected matrix from a non connected matrix
    '''
    nb_vertex = len(matrix)

    adjacency_matrix = np.asarray(matrix)
    np.fill_diagonal(adjacency_matrix, 1)

    # en theorie il faut mettre les poid a 1

    adjacency_matrix = matrix_power(adjacency_matrix, nb_vertex)

    rand_vertex = rand.randint(0, nb_vertex - 1)

    neighbour_to_connect = [index for index, value in enumerate(
        matrix[rand_vertex]) if value == 0 and index != rand_vertex]
    new_neighbour = rand.choice(neighbour_to_connect)

    # weight = 1
    weight = rand.randint(1, 100)

    matrix[rand_vertex][new_neighbour] = weight
    matrix[new_neighbour][rand_vertex] = weight

    return matrix


def Check_Matrix_Connected(matrix):
    '''
    Returns a boolean to check if an adjacency matrix matches a connected graph

    True : the graph is connected
    Fasle : the graph is not connected
    '''
    nb_vertex = len(matrix)

    adjacency_matrix = np.asarray(matrix)
    np.fill_diagonal(adjacency_matrix, 1)

    # for i in range(nb_vertex):
    #     for j in range(nb_vertex):
    #         if adjacency_matrix[i][j] != 0:
    #             adjacency_matrix[i][j] = 1

    adjacency_matrix = matrix_power(adjacency_matrix, nb_vertex)

    for line in adjacency_matrix:
        if not 0 in line:
            return True

    return False


def Get_Adjacency_Matrix(nb_vertex):
    '''
    Returns an order <nb_vertex> adjacene matrix
    '''
    matrix = [[0 for column in range(nb_vertex)] for row in range(nb_vertex)]

    completion_matrix = 10
    for row in range(nb_vertex):
        for column in range(nb_vertex):
            if rand.randint(1, 100) <= completion_matrix:
                weight = rand.randint(1, 100)

                matrix[row][column] = weight
                matrix[column][row] = weight

    while not Check_Matrix_Connected(matrix):
        matrix = Fix_Matrix_Not_Connected(matrix)

    for i in range(nb_vertex):
        matrix[i] = tuple(matrix[i])
    matrix = tuple(matrix)

    return matrix


# if __name__ == "__main__":