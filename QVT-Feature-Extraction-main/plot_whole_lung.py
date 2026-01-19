#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:23:12 2023

@author: 4o4notfound
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os.path import join
import os
from mayavi import mlab
import SimpleITK as sitk


def plot_tumor_and_lung_vessels(inpath):
    raw_features = pd.read_csv(join(inpath, 'features', 'raw_features.csv'))
    master_df = pd.read_pickle(join(inpath, 'master_df.pkl'))
    savepath = join(inpath, 'vis')
    tumves = sitk.ReadImage(join(inpath, 'Tumor_Vessels.nii.gz'))
    tumves = sitk.GetArrayFromImage(tumves).T
    tumor = np.uint8(tumves == 1)
    vessels = np.uint8(tumves == 2)
    vessels_img = sitk.ReadImage(join(inpath, 'Vessels.nii.gz'))
    lung_vessels = sitk.GetArrayFromImage(vessels_img).T

    # Create a new figure
    fig = mlab.figure(size=(1000, 800))
    fig.scene.background = (1, 1, 1)

    # Plot the tumor and lung vessels
    mlab.contour3d(tumor, color=(246 / 255, 210 / 255, 140 / 255), figure=fig)
    mlab.contour3d(lung_vessels, color=(215 / 255, 71 / 255, 31 / 255), opacity=0.2, figure=fig)

    mlab.view(azimuth=90, elevation=90, figure=fig)
    mlab.show()


if __name__ == '__main__':
    inpath = r'E:\GT\Research\NLST\Cohort1_T1_Cohort2_T2(flip_mask)\Python_Feature\Cohort2_QVT\106553'
    plot_tumor_and_lung_vessels(inpath)