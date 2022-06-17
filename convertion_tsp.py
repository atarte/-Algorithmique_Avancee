import shortest_path_Dijkstra as sp

def Convert_Tsp_to_Uncomplete_Graph():
    '''
    Returns
    '''
    
    return []


def Convert_Uncomplete_Graph_To_Tsp(matrix, cities):
    '''
    Returns a complete graph on the verteces that we want to visit that we will use to resolte Tsp from an uncomplete graph
    '''
    nb_vertex = len(matrix)
    new_matrix = [ [ 0 for column in range(nb_vertex)] for row in range(nb_vertex) ]

    for city in cities:
        shortest_path_to_city = sp.Shortest_Path(matrix, city)

        for i in range(nb_vertex):
            if city == i:
                continue

            if i in cities:
                new_matrix[city][i] = shortest_path_to_city[i]
                new_matrix[i][city] = shortest_path_to_city[i]

    return new_matrix

if __name__ == '__main__':
    matrix = [
        [0, 1, 0, 0],
        [1, 0, 2, 3],
        [0, 2, 0, 0],
        [0, 3, 0, 0],
    ]
    cities_to_pass = [0, 2, 3]
    print('matrix : ')
    for m in matrix:
        print(m)
    print('')

    short = sp.Shortest_Path(matrix, 0)
    print(short)
    print('')

    new_matrix = Convert_Tsp_to_Uncomplete_Graph(matrix, cities_to_pass)
    print('new matrix : ')
    for m in new_matrix:
        print(m)
    print('')


