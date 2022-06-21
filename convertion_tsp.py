import shortest_path_Dijkstra as sp

def Get_Full_Path_from_Tsp_Path(graph, path):
    '''
    Returns the full path from the path with only the city to pass
    '''
    full_path = [path[0]]

    for i in range(len(path) - 1):
        vertex_betwwen = sp.Path_Between_Two_Verteces(graph, path[i], path[i + 1])

        full_path += vertex_betwwen[1:]
    
    # return tuple(full_path)
    return full_path


def Convert_Uncomplete_Graph_To_Tsp(graph, nb_vertex, cities):
    '''
    Returns a complete graph on the verteces that we want to visit that we will use to resolte Tsp from an uncomplete graph
    '''
    # nb_vertex = len(graph)
    new_graph = [ [ 0 for column in range(nb_vertex)] for row in range(nb_vertex) ]

    for city in cities:
        shortest_path_to_city = sp.Shortest_Path(graph, city)

        for i in range(nb_vertex):
            if city == i:
                continue

            if i in cities:
                new_graph[city][i] = shortest_path_to_city[i]
                new_graph[i][city] = shortest_path_to_city[i]

    for i in range(nb_vertex):
        new_graph[i] = tuple(new_graph[i])
    new_graph = tuple(new_graph)

    return new_graph

# if __name__ == '__main__':

