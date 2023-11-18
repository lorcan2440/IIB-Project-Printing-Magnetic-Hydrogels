# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:21:37 2019

@author: Biointerface
"""

import numpy as np
A=np.array([0.1,0.1],[0.05,-0.95])
B=np.array([90,-5])
c=np.linalg.solve(A,B)
print (c)