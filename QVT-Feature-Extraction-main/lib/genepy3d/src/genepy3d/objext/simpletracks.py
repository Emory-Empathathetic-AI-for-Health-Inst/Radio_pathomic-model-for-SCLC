"""Methods for working with tracks.
"""

import numpy as np
from scipy.interpolate import splev, splrep
from genepy3d.obj import curves

def merge(tracklst):
    """Merge tracks. They must be placed in the increasing order of times.

    Args:
        tracklst (array of SimpleTrack): a list of SimpleTrack objects.

    Returns:
        A merged SimpleTrack object.

    """

    if len(tracklst)==1:
        return tracklst[0]
    else:
        coors, t = [], []
        coors.append(tracklst[0].coors) # initialize by the first track
        t.append(tracklst[0].time)
        for ix in range(1,len(tracklst)):
            if (tracklst[ix-1].time[-1] < tracklst[ix].time[0]): # check time order
                coors.append(tracklst[ix].coors)
                t.append(tracklst[ix].time)
            else:
                raise Exception("Time between tracks {} and {} is not in increasing order".format(ix-1,ix))
        
        coors = np.concatenate(coors,axis=0)
        t = np.concatenate(t,axis=0)
        return SimpleTrack(coors,t)

class SimpleTrack(curves.Curve):
    """A simple track object. 
    
    It's simple because it has no division or merge. 
    We can consider it as a Curve object with time attribute.
    
    Work in 3D but also support 2D tracks. Please check the documentation of each function to see if it supports 2D.

    Attributes:
        coors (array | tuple): array of points. See ``Curve`` for more detail.
        time (numeric): array of time.

    Examples:
        ..  code-block:: python

            import numpy as np
            from genepy3d.objext.simpletracks import SimpleTrack
            
            # Create SimpleTrack from array of points and time
            coors = np.array([[1,2,3],[1,2,3],[1,2,3]])
            t = np.array([1,2,3])
            track = SimpleTrack(coors,t)
    
    """

    def __init__(self, coors, t):
        super().__init__(coors)
        self.time = t

    def compute_time_gap(self):
        """Compute the difference between two consecutive times.

        Work in 3D and 2D.

        Returns:
            Array of time gap whose i element is the time gap between (ti, ti-1).

        Notes:
            The first element has no time gap and is set as np.nan.

        """

        time_shift = self.time[1:] - self.time[:-1]
        return np.array([np.nan] + list(time_shift))

    def split(self,max_gap):
        """Split track if the gap between two consecutive times is larger than max_gap.

        Work in 3D and 2D.

        Args:
            max_gap (float): maximual gap allowed between two consecutive times.

        Returns:
            List of subtracks.

        Examples:
            ..  code-block:: python

                import numpy as np
                from genepy3d.objext.simpletracks import SimpleTrack
                
                # Create SimpleTrack from array of points and time
                coors = np.array([[0,0,0],[1,1,1],[2,2,2],[1,1,1],[0,0,0]])
                t = np.array([0,1,2,10,11])
                track = SimpleTrack(coors,t)
                subtracks = track.split(max_gap=5) # the track is splitted in two tracks.

        """

        frameshift = self.compute_time_gap()
        breakidlst = np.argwhere(frameshift>max_gap).flatten()
        checkidlst = [0] + list(breakidlst) + [self.nb_of_points]
        
        subtracks = []
        for i in range(len(checkidlst)-1):
            subtracks.append(SimpleTrack(self.coors[checkidlst[i]:checkidlst[i+1]],self.time[checkidlst[i]:checkidlst[i+1]]))
        
        return subtracks
    
    def convolve_gaussian(self, sigma, mo="nearest", kerlen=4):
        """Overlay convolve_gaussian() of Curve object. 

        See more details of this function in ``Curve`` class.

        Work in 3D and 2D.

        Returns:
            SimpleTrack object.

        """
        crv_smoothed = super().convolve_gaussian(sigma, mo, kerlen)
        return SimpleTrack(crv_smoothed.coors,self.time)
    
    def resample(self, dt, spline_order=1, return_old_indices=False, return_interp_param=False):
        """The track is resampled by the new time step.

        Work in 3D and 2D.

        Args:
            dt (float|int): resampled time step.
            spline_order (int): degree of spline interpolation.
            return_old_indices (bool): if True, return the indices of new sampled time array correspond to the old time array.
            return_interp_param (bool): if True, return spline parameters.

        Returns:
            Resampled SimpleTrack object.

        Examples:
            ..  code-block:: python

                import numpy as np
                from genepy3d.objext.simpletracks import SimpleTrack
                
                # Create SimpleTrack from array of points and time
                coors = np.array([[0,0,0],[1,1,1],[2,2,2],[1,1,1],[0,0,0]])
                t = np.array([0,1,2,10,11])
                track = SimpleTrack(coors,t)
                track_new = track.resample(dt=1) # resample with time step = 1

        """

        # New number of spots
        n = int((self.time[-1]-self.time[0])/dt) + 1

        # New time
        time_new = np.linspace(self.time[0],self.time[-1],n)

        # Find from the new time the indices corresponding to the old time if possible
        if return_old_indices:
            old_ids = np.ones(len(self.time))*np.nan
            for ix in range(len(self.time)):
                ix2 = np.argwhere(self.time[ix]==time_new).flatten()
                if len(ix2)>0:
                    old_ids[ix] = ix2[0]

        # Compute spline parameters
        splx = splrep(self.time,self.coors[:,0],k=spline_order,s=0)
        sply = splrep(self.time,self.coors[:,1],k=spline_order,s=0)
        splz = splrep(self.time,self.coors[:,2],k=spline_order,s=0)

        # Compute new coordinates
        x_new = splev(time_new,splx)
        y_new = splev(time_new,sply)
        z_new = splev(time_new,splz)

        # New SimpleTrack
        track_resampled = SimpleTrack(np.array([x_new,y_new,z_new]).T,time_new)
        
        # Handle returns
        if (return_old_indices == False) & (return_interp_param == False):
            return track_resampled
        else:
            return_lst = [track_resampled]
            if return_old_indices:
                return_lst.append(old_ids)
            if return_interp_param:
                return_lst.append((splx,sply,splz))
            return return_lst

    
    def is_moving(self,num_neighbor,displ_tol):
        """Check if the object is moving at each point.

        Work in 3D and 2D.

        Args:
            num_neighbor (int): number of neighbor frames. The frames are used to check the movement at a frame n are [n-k,n-k-1,...,n,...,n+k-1,n+k], where k is the number of neighbors frames.
            displ_tol (float): if the displacement between neighbor points is larger than this value, then it's considered as no moving.

        Returns:
            Array of boolean with 0 = no moving, 1 = moving.

        """

        imflag = []
        frame_ids = np.arange(self.nb_of_points)

        for ix in frame_ids:
            
            ids = np.argwhere((frame_ids>=ix-num_neighbor)&(frame_ids<=ix+num_neighbor)).flatten()
            x = self.coors[ids,0]
            y = self.coors[ids,1]
            z = self.coors[ids,2]

            # compare min/max versus mean displacement in x, y and z
            dxmin = np.mean(x) - np.min(x)
            dxmax = np.max(x) - np.mean(x)

            dymin = np.mean(y) - np.min(y)
            dymax = np.max(y) - np.mean(y)

            dzmin = np.mean(z) - np.min(z)
            dzmax = np.max(z) - np.mean(z)

            flag = 0 # is immobile
            if (dxmin>displ_tol) | (dymin>displ_tol) | (dzmin>displ_tol) | (dxmax>displ_tol) | (dymax>displ_tol) | (dzmax>displ_tol):
                flag = 1 # is mobile  
            imflag.append(flag)

        return np.array(imflag)
    
    def compute_velocity(self):
        """Velocity at every point of the track.

        Work in 3D and 2D.

        Returns:
            Array of velocities.

        Notes:
            The first point has no velocity and is set as np.nan

        """

        velolst = [np.nan] # first frame has no velocity
        for ix in np.arange(1,self.nb_of_points):
            delta_t = self.time[ix] - self.time[ix-1]
            displacement = np.sqrt(np.sum((self.coors[ix] - self.coors[ix-1])**2))
            if delta_t == 0:
                velolst.append(np.nan)
            else:
                velolst.append(displacement/delta_t)

        return np.array(velolst)





