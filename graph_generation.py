from matplotlib import style
import numpy as np
from numpy.linalg import matrix_power
import random as rand
import matplotlib.pyplot as plt
import networkx as nx


def Init_Matrix(nb_vertex):
    '''
    Returns a null square matrix of order <nb_vertex>
    '''
    rows = nb_vertex
    cols = nb_vertex

    matrix = []
    for r in range(0, rows):
        matrix.append([0 for c in range(0, cols)])

    return matrix


def Fix_Matrix_Not_Connected(matrix):
    '''
    Returns a connected matrix from a non connected matrix
    '''
    print('fix matrix')

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
    weight = rand.randint(1, 10)

    matrix[rand_vertex][new_neighbour] = weight
    matrix[new_neighbour][rand_vertex] = weight

    return matrix


def Check_Matrix_Connected(matrix):
    '''
    Returns a boolean to check if an adjacency matrix matches a connected graph

    True : the graph is connected
    Fasle : the graph is not connected
    '''
    print('check matrix')

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


def Get_Neighbour_List(nb_vertex):
    '''
    Returns a list containning the number of neighbour each vertex will have
    '''
    order_min = (nb_vertex - 1) * 2
    order_max = (nb_vertex - 1) * nb_vertex
    nb_neighbour_max = nb_vertex - 1
    # nb_neighbour_max = 5/6 plutard
    nb_neighbour_min = 1
    # nb_neighbour_min = 2 plutard

    neighbour_list = []
    order_total = 1

    while order_total % 2 != 0 or order_total <= order_min or order_total >= order_max:
        neighbour_list = []

        for i in range(nb_vertex):
            neighbour_list.append([
                i,
                rand.randint(nb_neighbour_min, nb_neighbour_max),
            ])

        order_total = np.sum(neighbour_list, axis=0)[1]

    return neighbour_list


def Get_Adjacency_Matrix(nb_vertex):
    '''
    Returns an adjacene matrix for <nb_vertex> vertices
    '''
    matrix = Init_Matrix(nb_vertex)
    neighbour_list = Get_Neighbour_List(nb_vertex)
    neighbour_list_sorted = sorted(
        neighbour_list, key=lambda x: x[1], reverse=True)

    for vertex in neighbour_list_sorted:

        vertex_index = vertex[0]
        vertex_nb_neighbour = vertex[1]

        neighbour_allow = []

        for i in range(nb_vertex):

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

        vertex_neighbour_list = rand.sample(
            neighbour_allow, vertex_nb_neighbour)

        for vertex_neighbour in vertex_neighbour_list:
            # weight = 1
            weight = rand.randint(1, 10)

            matrix[vertex_index][vertex_neighbour] = weight
            matrix[vertex_neighbour][vertex_index] = weight

    while not Check_Matrix_Connected(matrix):
        matrix = Fix_Matrix_Not_Connected(matrix)

    return matrix


if __name__ == "__main__":
    nb_vertex = 6

    matrix = Get_Adjacency_Matrix(nb_vertex)
    # matrix = [
    #     [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [5, 0, 2, 8, 2, 8, 7, 10, 2, 0, 2, 2, 8, 7, 0],
    #     [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
    #     [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 2, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 9, 0, 7],
    #     [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 10, 0, 0, 0, 0, 0, 0, 0, 7, 9, 0, 4, 0, 4],
    #     [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 8, 0, 0, 7, 0, 0, 0, 0, 1, 0, 1],
    #     [0, 2, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 4, 0, 0],
    #     [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 8, 5, 0, 9, 0, 0, 4, 0, 1, 4, 0, 0, 0, 1],
    #     [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 7, 0, 0, 4, 0, 1, 0, 0, 1, 0, 0]
    # ]

    print('matrix : ')
    for m in matrix:
        print(m)

    G = nx.Graph()

    for i in range(nb_vertex):
        G.add_node(i, label=i, col='pink')

    for i in range(nb_vertex):
        for neighboor in range(i):
            for weight in range(matrix[i][neighboor]):
                if weight+1 > 0:
                    G.add_edge(i, neighboor, weight=weight+1, styl='solid')

    liste = list(G.nodes(data='col'))
    colorNodes = {}
    for noeud in liste:
        colorNodes[noeud[0]] = noeud[1]
    colorNodes

    colorList = [colorNodes[node] for node in colorNodes]
    colorList

    liste = list(G.nodes(data='label'))
    labels_nodes = {}
    for noeud in liste:
        labels_nodes[noeud[0]] = noeud[1]
    labels_nodes

    labels_edges = {}
    labels_edges = {edge: G.edges[edge]['weight'] for edge in G.edges}
    #labels_edges = {edge:'' for edge in G.edges}
    labels_edges

    # positions for all nodes
    pos = nx.spring_layout(G)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700,
                           node_color=colorList, alpha=0.9)

    # labels
    nx.draw_networkx_labels(G, pos, labels=labels_nodes,
                            font_size=20,
                            font_color='black',
                            font_family='sans-serif')

    # edges
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=labels_edges, font_color='red')

    plt.axis('off')
    plt.show()

    # print('')
    # IsMatrixConnected = Check_Matrix_Connected(matrix)
    # print('Is the matrix connected : ', IsMatrixConnected)
