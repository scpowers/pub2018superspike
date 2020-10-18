# file for testing out functionalities

import numpy as np
from helpers import *

# import matrix of coefficients from multiple trajectories
data = np.load('coeffs.npy')

# general approach: target_coeffs[i,j] = input_coeffs[i+1,j]
# thus, you can't use all coefficients for the input data

# define input and target coefficients
input_coeffs = data[0:-1, :]
target_coeffs = data[1:, :]

# for later use
print('Input matrix shape: ', input_coeffs.shape)
print('Target matrix shape: ', target_coeffs.shape)
numSteps = input_coeffs.shape[0]
numCoeffs = input_coeffs.shape[1]

# test that you selected the right data
print('input at t=i\n', input_coeffs[231,:])
print('target at t=i\n', target_coeffs[231,:])
print('target at t=i-1 (should match input):\n', target_coeffs[230,:])


# convert target values into a .ras file
ndarray2ras('randHeat-target', target_coeffs, 0, 4, 0.001)

# convert the created .ras file into an ndarray to ensure no corruption 
reconstructed_target = ras2ndarray('recon_randHeat_target', 'randHeat-target.ras', numCoeffs, 0, 4, 
        numSteps, 0.001)
print(np.amax(abs(reconstructed_target - target_coeffs)))

# convert input values into a .ras file
ndarray2ras('randHeat-input', input_coeffs, 0, 4, 0.001)

# convert the created .ras file into an ndarray to ensure no corruption 
reconstructed_input = ras2ndarray('recon_randHeat_input', 'randHeat-input.ras', numCoeffs, 0, 4, 
        numSteps, 0.001)
print(np.amax(abs(reconstructed_input - input_coeffs)))
