# -*- coding: utf-8 -*-
# Test module: points.py

import numpy as np
from genepy3d.obj import points

class TestPoints:
    """Basic test for Points class.
    """
    
    @staticmethod
    def get_simple_points():
        """Simulate simple point cloud.
        """
        
        ncol, nrow = 4, 3
        coors_grid = np.meshgrid(range(ncol),range(nrow))
        x = coors_grid[0].ravel()
        y = coors_grid[1].ravel()
        z = [10 for _ in x]
        coors = np.array([x,y,z]).T
        
        return points.Points(coors)
    
    def test_transform(self):
        
        cloud = self.get_simple_points()
        cloud_transformed = cloud.transform(psi=np.pi/2) # inverse clockwise direction
        assert np.round(cloud_transformed.coors[-1,0])==-2
        
    def test_fit_plane(self):
        cloud = self.get_simple_points()
        intercept, normal = cloud.fit_plane()
        assert np.round(intercept)==10.
        assert np.round(normal[0])==0.
        assert np.round(normal[1])==0.
        assert np.abs(np.round(normal[2]))==1.

    
def test_emd():
    """Test EMD func"""
    cloud = TestPoints.get_simple_points()
    assert points.emd(cloud,cloud)==0.
        

    
    
    
