# file for testing out functionalities

import numpy as np
from helpers import *
import pandas as pd
from sklearn.preprocessing import scale

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
