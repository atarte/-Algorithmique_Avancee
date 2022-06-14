import graph_generation as gg
import convertion_tsp as ct

import random as rand

def Get_Cities_To_Pass(nb_vertex, nb_cities_to_pass):
    '''
    Returns the list of cities through which the cycle must pass

    If the number of cities has passed is greater than the number of verteces then the number of cities to the number of verteces
    '''
    if nb_cities_to_pass > nb_vertex:
        nb_cities_to_pass = nb_vertex
        
    return rand.sample(range(nb_vertex), nb_cities_to_pass)

if __name__ == '__main__':
    nb_vertex = 10
    nb_cities_to_pass = 3

    cities_to_pass = Get_Cities_To_Pass(nb_vertex, nb_cities_to_pass)
    print(cities_to_pass)


