import shortest_path_Dijkstra as short

def Split_After_Tsp(graph, path, path_lenght, nb_truck):
    '''
    Split a path into a number of sub path
    '''
    starting_vertex = path[0]
    print(starting_vertex)

    aproximate_dist = path_lenght/nb_truck
    new_path = [[] for _ in range(nb_truck)]

    dist = 0
    current_path = 0

    for i in range(len(path)):
        new_path[current_path].append(path[i])
        
        if len(new_path[current_path]) < 2:
            continue

        dist += graph[path[i]][path[i - 1]]

        if dist >= aproximate_dist:
            current_path += 1
            dist = 0

    for i in range(nb_truck):

        first_vertex = new_path[i][0]
        last_vertex = new_path[i][len(new_path[i]) - 1]

        if first_vertex != starting_vertex:
            start_verteces = short.Path_Between_Two_Verteces(
                graph, starting_vertex, first_vertex)

            new_path[i] = start_verteces[:-1] + new_path[i]

        if last_vertex != starting_vertex:
            end_verteces = short.Path_Between_Two_Verteces(
                graph, last_vertex, starting_vertex)

            new_path[i] = new_path[i] + end_verteces[1:]

    return new_path
