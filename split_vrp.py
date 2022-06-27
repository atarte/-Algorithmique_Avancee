def Split_After_Tsp(graph, path, path_lenght, starting_point, nb_truck):
    '''
    Hej
    '''
    aproximate_dist = path_lenght/nb_truck
    new_path = tuple([starting_point] for _ in range(nb_truck))

    dist = 0
    current_path = 0

    for i in range(1, len(path) - 1):
        dist += graph[path[i]][path[i - 1]]
        new_path[current_path].append(path[i])

        if dist >= aproximate_dist:
            current_path += 1
            dist = 0

    for i in range(nb_truck):
        new_path[i].append(starting_point)

    return new_path
