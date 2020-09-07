# file for testing out functionalities

import numpy as np
from helpers import *

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

ndarray2ras('test', hard_test, 1, 3, 0.1)

ras2ndarray('tester_out', 'test-target.ras', 4, 1, 3, 5, 0.1)
