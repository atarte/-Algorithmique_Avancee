import experience_plan as expl
import graph_generation as gg
import convertion_tsp as ct
import matplotlib.pyplot as plt
import numpy as np
import main as mn
import time

def simplex_performance(nb_vertex, nb_test):
    current_Time = []
    Time = []
    for i in range(nb_test) :
        start = time.perf_counter()
        matrix = gg.Get_Adjacency_Matrix(nb_vertex)
        cities_to_pass = mn.Get_Cities_To_Pass(nb_vertex, nb_vertex)
        tsp_matrix = ct.Convert_Uncomplete_Graph_To_Tsp(matrix, nb_vertex, cities_to_pass)
        new_matrix = expl.Convert_to_complete(tsp_matrix, cities_to_pass)
        expl.Borne(nb_vertex, new_matrix)
        stop = time.perf_counter()
        total_time = stop - start
        current_Time.append(total_time)
    Time.append(np.mean(current_Time))
    print(Time)
    return Time



max_nb_vertex = range(3, 25, 10)
nb_test = 5
listTime = []
listSize = []

for i in max_nb_vertex :
    print(i)
    execTime = simplex_performance(i, nb_test)
    listTime.append(execTime)
    listSize.append(i)

plt.plot(listSize, listTime)
plt.xlabel("Number of cities", fontsize=16)
plt.ylabel("Execution Time", fontsize=16)
plt.show()





