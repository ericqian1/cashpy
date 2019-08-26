# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:48:23 2019

@author: eric.qian
"""

import numpy as np
from collections.abc import Iterable   # import directly from collections for Python < 3.3


class stream():
    

    """ Base class for all vectors """
    

    def __init__(self, 
                 vector = None, 
                 init_val = None, 
                 change = None, 
                 t = 1):
        
        self.init_val = init_val
        self.change = change
        self.t = t
        
        if vector is None:
            self.construct()
        
        self.vector = np.array(self.vector, dtype = np.float32)
        

    def construct(self):
        
        if hasattr(self.change, '__call__'):
            
            self.vector = [self.change(self.init_val, i) for i in range(self.t)]
            
        elif isinstance(self.change, Iterable):
            
            self.vector = self.init_val * self.change
            
        elif self.t and self.init_val and not self.change:
            
            self.vector = [self.init_val for i in range(self.t)]
            
        else:
            
            self.vector = []
            
            

