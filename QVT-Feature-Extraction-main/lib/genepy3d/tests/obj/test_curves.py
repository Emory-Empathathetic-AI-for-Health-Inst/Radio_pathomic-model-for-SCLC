# -*- coding: utf-8 -*-

import numpy as np
from genepy3d.obj import curves

class TestCurve:
    """Basic test of Curve class
    """
    
    @staticmethod
    def get_simple_curve():
        """Create a simple curve to test.
        """
        
        coors = np.array([[0., 0., 0.],
                          [1., 1., 0.],
                          [2., 2., 0.],
                          [3., 3., 0.],
                          [4., 3., 0.],
                          [5., 2., 0.]])
        
        return curves.Curve(coors)
    
    def test_compute_length(self):
        curve = self.get_simple_curve()
        assert curve.compute_length() == (4*np.sqrt(2)+1)
        
    def test_compute_torsion(self):
        curve = self.get_simple_curve()
        print(curve.compute_torsion())

        tau = curve.compute_torsion()
        assert np.sum(np.isnan(tau))==2
        assert np.sum(tau[~np.isnan(tau)])==0
        
    def test_compute_curvature(self):
        curve = self.get_simple_curve()
        kappa = curve.compute_curvature()
        assert kappa[3]==kappa[4]
    
    def test_compute_angle(self):
        
        curve = self.get_simple_curve()
        angles = curve.compute_angles()
        angles = np.round(angles*180/np.pi,0)
                
        assert angles[1] == 180
        assert angles[3] == 135
        assert angles[4] == 135
        
    def test_compute_tortuosity(self):
        curve = self.get_simple_curve()
        assert curve.compute_tortuosity()==((4*np.sqrt(2)+1)/(np.sqrt(5**2+2**2)))

    def test_main_turns(self):
        curve = self.get_simple_curve()
        curve.coors = np.append(curve.coors,[[7.,0.,0.]],axis=0)
        sig_lst = np.arange(0,1+0.25,0.25)
        ids = curve.main_turns(sig_lst)
        assert ids[0]==4


        
    
    

    
    
