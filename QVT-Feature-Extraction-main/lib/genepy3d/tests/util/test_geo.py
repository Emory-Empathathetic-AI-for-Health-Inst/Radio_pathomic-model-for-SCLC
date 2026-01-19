# -*- coding: utf-8 -*-
# test io.swc module

from genepy3d.util import geo
import numpy as np

def test_emd():
    n = 3
    x = np.array([[1. for _ in range(n)],range(1,n+1),[0. for _ in range(n)]]).T
    y = np.array([[2. for _ in range(n)],range(1,n+1),[0. for _ in range(n)]]).T
    loss = geo.emd(x,y)    
    assert loss==1.

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    