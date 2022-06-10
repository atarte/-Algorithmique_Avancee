import random

def Init_Weight_Matrix(nb_Vertex):
    rows = nb_Vertex
    cols = nb_Vertex

    matrix = []
    for r in range(0, rows):
        matrix.append([0 for c in range(0, cols)])

    return matrix


if __name__ == "__main__":
    nb_Vertex = 4
    nb_Neighbourg_Max = 3
    
    weight_Matrix = Init_Weight_Matrix(nb_Vertex)






    print('end')


