import sys

def Min_Distance(dist, sptSet):
    '''
    Return the vertex with minimum distance value, from the set of vertices not yet included in shortest path tree
    '''
    nb_vertex = len(dist)
    min = sys.maxsize
    
    for v in range(nb_vertex):
        if dist[v] < min and sptSet[v] == False:
            min = dist[v]
            min_index = v

    return min_index

def Shortest_Path(graph, starting_vertex):
    '''
    Returns the list of shortest distances between one vertex <starting_vertex> and all other vertices of the graph 
    '''
    nb_vertex = len(graph)
    dist = [sys.maxsize] * nb_vertex
    dist[starting_vertex] = 0
    sptSet = [False] * nb_vertex

    for cout in range(nb_vertex):
        u = Min_Distance(dist, sptSet)
        sptSet[u] = True
        
        for v in range(nb_vertex):
            if graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + graph[u][v]:
                dist[v] = dist[u] + graph[u][v]

    return dist


def Path_Between_Two_Verteces(graph, vertex_1, vertex_2):
    '''
    Returns  
    '''
    nb_vertex = len(graph)
    dist = [sys.maxsize] * nb_vertex
    dist[vertex_1] = 0
    sptSet = [False] * nb_vertex

    path = [[]] * nb_vertex
    # path[starting_vevertex_1rtex] = [starting_vertex, [starting_vertex]]
    path[vertex_1] = [vertex_1]

    for cout in range(nb_vertex):
        u = Min_Distance(dist, sptSet)
        sptSet[u] = True

        stop = False

        for v in range(nb_vertex):
            if graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + graph[u][v]:
                dist[v] = dist[u] + graph[u][v]
                
                # path[v] = [dist[v], path[u][1] + [v]]
                path[v] = path[u] + [v]

                if v == vertex_2:
                    stop = True
                    break
        if stop:
            break
    
    return path[vertex_2]


if __name__ == '__main__':
    # matrix = [ 
    #     [0, 4, 0, 0, 0, 0, 0, 8, 0],
    #     [4, 0, 8, 0, 0, 0, 0, 11, 0],
    #     [0, 8, 0, 7, 0, 4, 0, 0, 2],
    #     [0, 0, 7, 0, 9, 14, 0, 0, 0],
    #     [0, 0, 0, 9, 0, 10, 0, 0, 0],
    #     [0, 0, 4, 14, 10, 0, 2, 0, 0],
    #     [0, 0, 0, 0, 0, 2, 0, 1, 6],
    #     [8, 11, 0, 0, 0, 0, 1, 0, 7],
    #     [0, 0, 2, 0, 0, 0, 6, 7, 0], 
    # ]
    matrix = [
        [0, 1, 0, 0],
        [1, 0, 2, 3],
        [0, 2, 0, 0],
        [0, 3, 0, 0],
    ]

    print('matrix : ')
    for m in matrix:
        print(m)
    print('')

    short = Shortest_Path(matrix, 0)
    print(short)
