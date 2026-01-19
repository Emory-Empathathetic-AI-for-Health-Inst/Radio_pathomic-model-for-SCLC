# -*- coding: utf-8 -*-
# test io.trackmate module

import os
from genepy3d.io import trackmate

def test_read_spots():
    filepath = os.path.join("tests","data","trackmate","Spots.csv")
    obj = trackmate.read_spots(filepath)

    assert obj.nb_tracks==2

    assert obj.tracks_nb_spots().loc[0] == 242

    assert obj.tracks_nb_spots().loc[1] == 292

    assert obj.get_tracks(0).nb_of_points == 242

    obj.remove_tracks([0])
    assert obj.nb_tracks == 1