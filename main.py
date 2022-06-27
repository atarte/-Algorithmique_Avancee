import graph_generation as gg
import convertion_tsp as ct
import tsp_ant as ant
# import shortest_path_Dijkstra as short
import experience_plan as expl

from matplotlib import style
# from random import sample
import random as rand
import matplotlib.pyplot as plt
import networkx as nx
import time
# import functools


def Get_Cities_To_Pass(nb_vertex, nb_cities_to_pass):
    '''
    Returns the list of cities through which the cycle must pass

    If the number of cities has passed is greater than the number of verteces then the number of cities to the number of verteces
    '''
    if nb_cities_to_pass > nb_vertex:
        nb_cities_to_pass = nb_vertex
    elif nb_cities_to_pass < 0:
        nb_cities_to_pass = 0
        
    return tuple(rand.sample(range(nb_vertex), nb_cities_to_pass))


def Draw_Graph(graph, cities_to_pass=[], path=[]):
    '''
    Draw a graph from an adjacency matrix
    '''
    G = nx.Graph()

    for i in range(nb_vertex):
        if sum(graph[i]) != 0:
            if i in cities_to_pass:
                G.add_node(i, label=i, col='red')
            else:
                G.add_node(i, label=i, col='pink')

    for row in range(nb_vertex):
        for column in range(row):
            if graph[row][column] != 0:
                if any([row, column] == path[i:i+2] for i in range(len(path) - 1)) or any([column, row] == path[i:i+2] for i in range(len(path) - 1)):
                    G.add_edge(
                        row, column, weight=graph[row][column], color='red', styl='solid')
                else:
                    G.add_edge(
                        row, column, weight=graph[row][column], color='black', styl='solid')

    liste = list(G.nodes(data='col'))
    colorNodes = {}
    for noeud in liste:
        colorNodes[noeud[0]] = noeud[1]
    # colorNodes

    colorListNode = [colorNodes[node] for node in colorNodes]
    # colorListNode

    liste = list(G.nodes(data='label'))
    labels_nodes = {}
    for noeud in liste:
        labels_nodes[noeud[0]] = noeud[1]
    # labels_nodes

    edges = G.edges()
    labels_edges = {}
    labels_edges = {edge: G.edges[edge]['weight'] for edge in G.edges}
    colors = [G[u][v]['color'] for u, v in edges]
    #labels_edges = {edge:'' for edge in G.edges}
    # labels_edges

    # positions for all nodes
    pos = nx.spring_layout(G)
    # pos = nx.circular_layout(G)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700,
                           node_color=colorListNode, alpha=0.9)

    # labels
    nx.draw_networkx_labels(G, pos, labels=labels_nodes,
                            font_size=20,
                            font_color='black',
                            font_family='sans-serif')

    # edges
    nx.draw_networkx_edges(G, pos, width=1, edge_color=colors)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=labels_edges, font_color='red')

    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # rand.seed(a=3)

    nb_vertex = 231
    nb_cities_to_pass = 231
    nb_test = 1

    start = time.process_time()
    matrix = gg.Get_Adjacency_Matrix(nb_vertex)

    cities_to_pass = Get_Cities_To_Pass(nb_vertex, nb_cities_to_pass)
    # print(cities_to_pass)

    tsp_matrix = ct.Convert_Uncomplete_Graph_To_Tsp(matrix, nb_vertex, cities_to_pass)

    path, path_lenght = ant.Ant_Tsp(tsp_matrix, cities_to_pass)

    # info1 = ant.Ant_Tsp.cache_info()
    # info2 = ant.Get_Path_Lenght.cache_info()
    # print(info1)
    # print(info2)

    print('optimal path : ', path)
    print('optimal path lenght : ', path_lenght)

    #  Draw_Graph(tsp_matrix, cities_to_pass=cities_to_pass, path=path)

    full_path = ct.Get_Full_Path_from_Tsp_Path(matrix, path)
    print(full_path)
    stop = time.process_time()
    print("calculé en ", stop-start, 's')

    # for i in range(237):
    #     matrix[i] = tuple(matrix[i])

    # expl.Optimal_parameters(tsp_matrix, cities_to_pass, nb_test)

    # Draw_Graph(matrix, cities_to_pass=cities_to_pass, path=full_path)

    


