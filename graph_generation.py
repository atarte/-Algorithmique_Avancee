import numpy as np
import random as rand

def Init_Matrix(nb_Vertex):
    '''
    Returns a null square matrix of order <nb_Vertex>
    '''
    rows = nb_Vertex
    cols = nb_Vertex

    matrix = []
    for r in range(0, rows):
        matrix.append([0 for c in range(0, cols)])

    return matrix


def Check_Matrix_Connected(matrix):
    '''
    Returns a boolean to check if an adjacency matrix matches a connected graph

    True : the graph is connected
    Fasle : the graph is not connected
    '''
    return true


def Get_Neighbour_List(nb_Vertex):
    '''
    Returns a list containning the number of neighbour each vertex will have
    '''
    order_min = (nb_Vertex - 1) * 2
    order_max = (nb_Vertex - 1) * nb_Vertex
    nb_neighbour_max = nb_Vertex - 1
    # nb_neighbour_max = 5/6 plutard
    nb_neighbour_min = 1
    # nb_neighbour_min = 2 plutard

    neighbour_list = []
    order_total = 1

    while order_total % 2 != 0 or order_total <= order_min or order_total >= order_max:
        neighbour_list = []

        for i in range(nb_Vertex):
            neighbour_list.append([
                i,
                rand.randint(nb_neighbour_min, nb_neighbour_max),
            ])

        order_total = np.sum(neighbour_list, axis=0)[1]
    
    return neighbour_list


def Get_Adjacency_Matrix(nb_Vertex):
    '''
    Returns an adjacene matrix for <nb_Vertex> vertices
    '''
    matrix = Init_Matrix(nb_Vertex)
    neighbour_list = Get_Neighbour_List(nb_Vertex)
    neighbour_list_sorted = sorted(neighbour_list, key=lambda x:x[1], reverse=True)

    # Fill the adjacencie matrix
    for vertex in neighbour_list_sorted:

        vertex_index = vertex[0]
        vertex_nb_neighbour = vertex[1]

        neighbour_allow = []

        for i in range(nb_Vertex):

            if i == vertex_index:
                continue

            if matrix[vertex_index][i] != 0:
                vertex_nb_neighbour -= 1
                continue

            if np.sum(matrix, axis=1)[i] >= neighbour_list[i][1]:
                continue

            neighbour_allow.append(i)

        if vertex_nb_neighbour <= 0:
            continue
        
        if vertex_nb_neighbour > len(neighbour_allow):
            vertex_nb_neighbour = len(neighbour_allow)

        vertex_neighbour_list = rand.sample(neighbour_allow, vertex_nb_neighbour)

        for vertex_neighbour in vertex_neighbour_list:

            matrix[vertex_index][vertex_neighbour] = 1 # le poid plutard
            matrix[vertex_neighbour][vertex_index] = 1 # le poid plutard
    
    return matrix
    

if __name__ == "__main__":
    nb_Vertex = 6

    matrix = Get_Adjacency_Matrix(nb_Vertex)

    print('matrix : ')
    for m in matrix:
        print(m)






    print('end')


