import numpy as np
import matplotlib.pyplot as plt

size = 100
N = (size-2)**2

Matrix = np.zeros((N, N))


def set_diagonal(Matrix):
    for i in range(N):
        for j in range(N):
            if i == j:
                Matrix[i][j] = -4
    return Matrix


FunctionMatrix = set_diagonal(Matrix)

# Set boundary temperatures
T_top = 100
T_bottom = 1000
T_left = 50
T_right = 300

# create 2d matrix of zeros
Plate = np.zeros((size, size))

# set boundary conditions
Plate[:1] = T_top
Plate[-1:] = T_bottom
Plate[:, :1] = T_right
Plate[:, -1:] = T_left
Plate[0, 0] = (T_top + T_right)/2
Plate[0, -1] = (T_top + T_left)/2
Plate[-1, 0] = (T_bottom + T_right)/2
Plate[-1, -1] = (T_bottom + T_left)/2


def Find_Ones(Matrix):
    Ones = np.zeros((N, N))
    ones_index = 0
    for i in range(size-2):
        for j in range(size-2):
            if i == 0 and j == 0:
                neighbours = [[i+1, j], [i, j+1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
            elif i == 0 and j == size-3:
                neighbours = [[i+1, j], [i, j-1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
            elif i == size-3 and j == 0:
                neighbours = [[i-1, j], [i, j+1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
            elif i == size-3 and j == size-3:
                neighbours = [[i-1, j], [i, j-1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
            elif i == 0 and j > 0 and j < size-3:
                neighbours = [[i+1, j], [i, j-1], [i, j+1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
            elif i == size-3 and j > 0 and j < size-3:
                neighbours = [[i-1, j], [i, j-1], [i, j+1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
            elif j == 0 and i > 0 and i < size-3:
                neighbours = [[i-1, j], [i+1, j], [i, j+1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
            elif j == size-3 and i > 0 and i < size-3:
                neighbours = [[i-1, j], [i+1, j], [i, j-1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
            else:
                neighbours = [[i-1, j], [i+1, j], [i, j-1], [i, j+1]]
                for element in neighbours:
                    index = element[0] * (size-2) + element[1]
                    Ones[ones_index][index] = 1
                ones_index += 1
    return Ones


Ones = Find_Ones(Plate)
FinalMatrix = Ones + Matrix

Boundary = np.zeros((N, 1))
for i in range(size-2):
    for j in range(size-2):
        if i == j == 0:
            Boundary[i*(size-2)+j] = -(T_top + T_right)
        elif i == 0 and j < size - 3:
            Boundary[i*(size-2)+j] = -T_top
        elif i == size - 3 and j < size-3:
            Boundary[i*(size-2)+j] = -T_bottom
        elif i == 0 and j == size - 3:
            Boundary[i*(size-2)+j] = -(T_top + T_left)
        elif i < size - 3 and j == 0:
            Boundary[i*(size-2)+j] = -T_right
        elif i < size - 3 and j == size - 3:
            Boundary[i*(size-2)+j] = -T_left
        elif i == size - 3 and j == 0:
            Boundary[i*(size-2)+j] = -(T_bottom + T_right)
        elif i == size - 3 and j == size - 3:
            Boundary[i*(size-2)+j] = -(T_bottom + T_left)
        else:
            Boundary[i*(size-2)+j] = 0


Temps_calc = np.dot(np.linalg.inv(FinalMatrix), Boundary)
for element in range(len(Temps_calc)):
    Temps_calc[element] = float(Temps_calc[element])
Temps_calc = Temps_calc.reshape(size-2, size-2)

# overlay calculated temperatures on plate
Plate[1:-1, 1:-1] = Temps_calc

plt.imshow(Plate.reshape(size, size),
           cmap='coolwarm', interpolation="nearest")
plt.imsave('Plate.png', Plate.reshape(size, size), cmap='coolwarm')
