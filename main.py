import graph_generation as gg
import convertion_tsp as ct
import tsp_ant as ant
# import shortest_path_Dijkstra as short
import experience_plan as expl
import split_vrp as split

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


def Draw_Graph(graph, weighted=False, cities_to_pass=[], path=[]):
    '''
    Draw a graph from an adjacency matrix
    '''
    G = nx.Graph()
    nb_vertex = len(graph)

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
    # pos = nx.random_layout(G)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=500,
                           node_color=colorListNode, alpha=0.9)

    # labels
    nx.draw_networkx_labels(G, pos, labels=labels_nodes,
                            font_size=15,
                            font_color='black',
                            font_family='sans-serif')

    # edges
    nx.draw_networkx_edges(G, pos, width=1, edge_color=colors)
    
    if weighted:
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=labels_edges, font_color='red')

    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # rand.seed(a=3)
    # nb_test = 1
    # expl.Optimal_parameters(tsp_matrix, cities_to_pass, nb_test)

    nb_vertex = 20
    nb_cities_to_pass = 10
    nb_truck = 3

    # Generate Graph
    start = time.process_time()
    matrix = gg.Get_Adjacency_Matrix(nb_vertex)
    print('matrix : ')
    for m in matrix:
        print(m)
    print()
    
    Draw_Graph(matrix, weighted=True)

    # Get the citie to pass
    cities_to_pass = Get_Cities_To_Pass(nb_vertex, nb_cities_to_pass)
    print('citie to pass : ', cities_to_pass)
    print()

    Draw_Graph(matrix, cities_to_pass=cities_to_pass)

    # Solve with ACO
    tsp_matrix = ct.Convert_Uncomplete_Graph_To_Tsp(matrix, nb_vertex, cities_to_pass)

    path, path_lenght = ant.Ant_Tsp(tsp_matrix, cities_to_pass)
    # print('optimal path : ', path)
    print('optimal path lenght : ', path_lenght)

    full_path = ct.Get_Full_Path_from_Tsp_Path(matrix, path)
    print('optimal path : ', full_path)
    print()

    Draw_Graph(matrix, cities_to_pass=cities_to_pass, path=full_path)

    # Split the path
    cluster_path = split.Split_After_Tsp(matrix, full_path, path_lenght, nb_truck)

    for i in range(len(cluster_path)):
        cluster_lenght = ant.Get_Path_Lenght(matrix, tuple(cluster_path[i]))
        print('truck n°', i + 1, ', path lenght : ', cluster_lenght)
        print('path : ', cluster_path[i])

        Draw_Graph(matrix, cities_to_pass=cities_to_pass, path=cluster_path[i])


    


