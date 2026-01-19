# -*- coding: utf-8 -*-

import numpy as np
from genepy3d.objext import simpletracks


def get_simple_track():
    """Create a simple track to test.
    """
    # Hexagon
    r = 5
    thetas = np.array([2*np.pi/6 * ix for ix in range(1,7)])
    x1 = (r * np.cos(thetas)).astype(np.int64)
    y1 = (r * np.sin(thetas)).astype(np.int64)
    t1 = np.arange(len(x1))
    
    # zig-zag
    x2 = np.arange(15,21)
    y2 = np.array([-3,3,-3,3,-3,3])
    t2 = np.arange(15,15+len(y2))
    
    # immobile
    x3 = np.ones(15)*21
    y3 = np.ones(15)*4
    t3 = np.arange(27,27+len(y3))
    
    x = np.concatenate([x1,x2,x3])
    y = np.concatenate([y1,y2,y3])
    t = np.concatenate([t1,t2,t3])
    tracksimu = simpletracks.SimpleTrack(np.array([x,y]).T,t)
    
    return tracksimu

def test_simpletrack():
    track = get_simple_track()

    assert track.nb_of_points==27

    # tetst split
    subtracks = track.split(5)
    assert len(subtracks)==3
    assert subtracks[0].nb_of_points == 6
    assert subtracks[1].nb_of_points == 6
    assert subtracks[2].nb_of_points == 15

    # test immobile
    track3 = subtracks[2]
    mobile_flag = track3.is_moving(3,0.5)
    assert np.sum(mobile_flag)==0

    # test velocity
    velo = track3.compute_velocity()
    assert np.sum(velo[1:]) == 0.

    # test resample
    track1 = subtracks[0]
    track1_resampled, old_ids = track1.resample(0.5, return_old_indices=True)
    assert track1_resampled.nb_of_points == 2 * track1.nb_of_points - 1

def test_merge():
    """Test merge tracks"""

    track = get_simple_track()
    subtracks = track.split(5)
    track_merged = simpletracks.merge(subtracks)
    assert track_merged.nb_of_points == track.nb_of_points