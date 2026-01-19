import numpy as np
from genepy3d.obj import surfaces

class TestSurface:
    """Basic test for Surface class.
    """
    
    @staticmethod
    def get_coors():
        """Simulate simple coordinates.
        """
        coors = np.array([
            [0,0,0],
            [1,0,0],
            [1,1,0],
            [0,1,0],
            [0,0,1],
            [1,0,1],
            [1,1,1],
            [0,1,1],
            [0.5,0.,0.5],
            [1.,0.5,0.5],
            [0.5,1.,0.5],
            [0.,0.5,0.5],
            [0.5,0.5,0.],
            [0.5,0.5,1.],
            [0.5,0.5,0.5]
        ])
        return coors      
    
    def test_qhul(self):
        surf = surfaces.Surface.from_points_qhull(self.get_coors())
        assert surf.vertices.shape[0]==8 # 8 points of cube
        assert surf.faces.shape[0]==12 # 12 triangle faces

    