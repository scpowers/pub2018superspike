# file for testing out functionalities

import numpy as np
from helpers import *
import pandas as pd
from sklearn.preprocessing import scale

# simple tester arrays
'''
testMatrix = np.array([[0.00, 0.00, 0.00],
                       [-1.11, -1.11, -1.11],
                       [-2.45, 1.39, 2.98]])

simple_test = np.array([[0.001],
                        [-2.412],
                        [5.163],
                        [1.874],
                        [3.395]])

medium_test = np.array([[0.001, 0.001],
                        [-2.412, -2.412],
                        [5.163, 5.163],
                        [1.874, 1.874],
                        [3.395, 3.395]])

hard_test = np.array([[1.015, -2.001, 0.512, 2.025],
                        [-2.412, 5.310, -5.555, -1.234],
                        [5.163, 0.193, -0.212, 5.695],
                        [0.855, 1.874, -1.112, 9.145],
                        [3.395, -3.395, 0.154, 0.246]])
'''
# import wine quality data
data = np.genfromtxt('winequality-red_noHeader.csv', delimiter=';')

# split data into features (x) and target (y)
x = data[:, 0:11]
y = data[:, 11]

# print first wine's stats and quality
print(y[0])
print(x[0,:])

# center and scale the features
x = scale(x)

# reshape target into a 1599,1 shape array instead of 1599,
y = y.reshape((1599,1))
#print(y.shape)
#print(y[0:10])


# convert target values (quality) into a .ras file
ndarray2ras('wine-target', y, 0, 0, 0.1)

# convert the created .ras file into an ndarray to ensure no corruption 
reconstructed_target = ras2ndarray('recon_wine_target', 'wine-target.ras', 1, 0, 0, 1599, 0.1)
print(max(abs(reconstructed_target - y)))

# convert features into a .ras file
ndarray2ras('wine-input', x, 1, 3, 0.1)

# convert the created .ras file into an ndarray to ensure no corruption 
reconstructed_input = ras2ndarray('recon_wine_input', 'wine-input.ras', 11, 1, 3, 1599, 0.1)
print(np.amax(abs(reconstructed_input - x)))
