#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 22:26:39 2024

@author: 4o4notfound
"""

from genepy3d.obj import curves
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import gaussian
from scipy import stats
from fractal_dimension import anisotropic_fractal_dimension
from radiomics import cShape
import os
import networkx as nx
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm
from sklearn.linear_model import HuberRegressor
from os.path import join
from scipy import ndimage as ndi

class compute_features:
    def __init__(self, qvt):
        self.master_df = qvt.master_df
        self.npaths = qvt.npaths
        self.spacing = qvt.spacing
        self.G = qvt.G
        self.SG = qvt.SG
        self.Vessels_PT = qvt.Vessels_PT
        self.skeleton = qvt.skeleton
        self.savepath = qvt.savepath
#
        self.initialize()
        self.branch_measurements()
        self.direction_angle()
        self.compute_genepy_feats()
        self.mask_features()
#
        self.feature_vector()

    def initialize(self):
        self.branch_features = self.master_df.copy()
        self.branch_features = self.branch_features.drop(columns=['coords', 'StartPoint', 'EndPoint', 'spline_coords', 'spline_derivative',
                                                                  'edt_values_spline', 'cumulative_distance_bw_points'])
        self.stats = ['mean', 'median', 'std', 'iqr', 'min', 'max', 'skew', 'kurt']
        f = ['curvature', 'torsion']
        self.genepy_feats = [i+'_'+j for i in f for j in self.stats]
        self.direction_angle_feats = ['direction_angle'+i for i in self.stats]
        self.new_feats = ['tumor_feeding', 'diameter', 'length', 'tortuosity', *self.genepy_feats, *self.direction_angle_feats]

        for col in self.new_feats:
            self.branch_features[col] = np.nan

    def feature_vector(self):
        print("Extracting overall features")
        df_feats = self.branch_features.iloc[:,5:]

        final_cols = df_feats.columns.tolist()
        final_cols = [i+'_'+j for i in final_cols for j in self.stats]
        self.final_cols = [*final_cols, 'num_tumorfeeding', 'prop_tumorfeeding', 'fractal_mask', 'fractal_skel', 'meshvol', 'voxelvol', 'surfacearea', 'surfvolumeratio']
        num_tum_feeding = np.sum(self.branch_features['tumor_feeding'])
        prop_tum_feeding = np.divide(num_tum_feeding, np.sum(self.master_df['valid']))

        feat_vec = np.array([self.compute_statistics(df_feats[i].to_list()) for i in df_feats.columns.tolist()]).flatten().tolist()
        feat_vec = [*feat_vec, num_tum_feeding, prop_tum_feeding, self.fractal_mask, self.fractal_skel, *self.pyrad_feats]
        self.feat_vec = pd.DataFrame(feat_vec).T
        self.feat_vec.columns = self.final_cols

        os.makedirs(os.path.join(self.savepath, 'features'), exist_ok=True)
        self.branch_features.to_csv(join(self.savepath, 'features', 'raw_features.csv'), index=False)
        self.feat_vec.to_csv(join(self.savepath, 'features', 'overall_features.csv'), index=False)

    def branch_measurements(self):
        dilated_SG = ndi.binary_dilation(self.SG, iterations=2)
        for i in range(self.npaths):
            if self.master_df.iloc[i]['valid']==0:
                continue
            self.branch_features.loc[i, 'length'] = self.master_df.iloc[i]['cumulative_distance_bw_points'][-1]
            self.branch_features.loc[i, 'diameter'] = np.nanmedian(self.master_df.iloc[i]['edt_values_spline'])
            self.branch_features.loc[i, 'tumor_feeding'] = 0
            for cur_coord in self.master_df.iloc[i]['coords']:
                if dilated_SG[cur_coord[0], cur_coord[1], cur_coord[2]] == 1:
                    self.branch_features.loc[i, 'tumor_feeding'] = 1

    def direction_angle(self, plot=False):
        if plot:
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
        for i in range(self.npaths):
            cur_df = self.master_df.iloc[i]
            valid_branch = cur_df['valid']
            if valid_branch:
                StartPoint = cur_df['spline_coords'][0]
                EndPoint = cur_df['spline_coords'][-1]
                main_vec2 = EndPoint - StartPoint
                norm = np.linalg.norm(main_vec2)
                main_vec = (main_vec2 / norm)
                v2 = np.multiply(cur_df['spline_derivative'], self.spacing)
                dot_product = [np.dot(main_vec, i) for i in v2]
                norm_v1 = np.linalg.norm(main_vec)
                norm_v2 = np.linalg.norm(v2, axis=1)
                cos_angle = dot_product / (norm_v1 * norm_v2)
                angles = np.degrees(np.arccos(cos_angle))
                if plot:
                    ax.plot(cur_df['spline_coords'][:,0], cur_df['spline_coords'][:,1], cur_df['spline_coords'][:,2], label=i)
                    ax.quiver(StartPoint[0], StartPoint[1], StartPoint[2], main_vec2[0], main_vec2[1], main_vec2[2], color='r', arrow_length_ratio=0.1)
                    ax.quiver(cur_df['spline_coords'][:,0], cur_df['spline_coords'][:,1], cur_df['spline_coords'][:,2], main_vec[0], main_vec[1], main_vec[2], color='r', arrow_length_ratio=0.1)
                    ax.quiver(cur_df['spline_coords'][:,0], cur_df['spline_coords'][:,1], cur_df['spline_coords'][:,2], v2[:,0], v2[:,1], v2[:, 2], color='g', arrow_length_ratio=0.1)
                tortuosity_angle = self.compute_statistics(angles)
            else:
                tortuosity_angle = [np.nan] * 8
            for j,col in enumerate(self.direction_angle_feats):
                self.branch_features.loc[i, col] = tortuosity_angle[j] if valid_branch else np.nan

    def get_genepy_features(self, coords):
        curve = curves.Curve(coords)
        curvature = curve.compute_curvature()
        torsion = curve.compute_torsion()
        torsion = gaussian(torsion,sigma=1.)
        tortuosity = curve.compute_tortuosity()
#        res = curve.scale_space([2.5, 5],features={"curvature","torsion"})
#        curvature_2_5 = res['curvature'][0]
#        torsion_2_5 = res['torsion'][0]
#        curvature_5 = res['curvature'][1]
#        torsion_5 = res['torsion'][1]
        return [tortuosity, *self.compute_statistics(curvature), *self.compute_statistics(torsion)]

    def compute_genepy_feats(self):
        tortuosity_feats = ['tortuosity', *self.genepy_feats]
        print("\nExtracing tortuosity...")
        for i in range(self.npaths):
            cur_coords = self.master_df['spline_coords'][i]
            valid = self.master_df['valid'][i]
            genepy_feats = self.get_genepy_features(cur_coords) if valid else [np.nan]*17
            for j,col in enumerate(tortuosity_feats):
                self.branch_features.loc[i, col] = genepy_feats[j] if valid else np.nan

    def mask_features(self):
        self.fractal_mask = anisotropic_fractal_dimension(self.Vessels_PT, self.spacing)
        self.fractal_skel = anisotropic_fractal_dimension(self.skeleton, self.spacing)
        self.pyrad_feats = self.pyrads()

    def pyrads(self):
        mask = self.crop_non_zero_region(self.Vessels_PT.copy())
        surfacearea, meshvol, diameters = cShape.calculate_coefficients(mask, self.spacing)
        voxelvol = np.sum(mask>0) * np.prod(self.spacing)
        surfvolumeratio = surfacearea / meshvol
        pyrad_shape = [meshvol, voxelvol, surfacearea, surfvolumeratio]
        return pyrad_shape

    def crop_non_zero_region(self, mask):
        # Identifying the indices of non-zero elements
        non_zero_coords = np.argwhere(mask)
        # If there are no non-zero elements, return the original mask
        if non_zero_coords.shape[0] == 0:
            return mask
        # Determine the bounding box
        min_coords = non_zero_coords.min(axis=0)
        max_coords = non_zero_coords.max(axis=0) + 1  # add 1 for inclusive slicing
        # Cropping the mask
        cropped_mask = mask[min_coords[0]:max_coords[0],
                            min_coords[1]:max_coords[1],
                            min_coords[2]:max_coords[2]]
        return cropped_mask

    def angle(self, start1, end1, start2, end2):
        v1 = np.subtract(end1, start1)
        v2 = np.subtract(end2, start2)
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        cos_angle = dot_product / (norm_v1 * norm_v2)
        return np.degrees(np.arccos(cos_angle))

    def graph_features(self):
        pass

    def compute_statistics(self, array):
        return [np.nanmean(array), np.nanmedian(array), np.nanstd(array), stats.iqr(array, nan_policy='omit'), np.nanmin(array), np.nanmax(array),
                stats.skew(array, axis=None, nan_policy='omit'), stats.kurtosis(array, axis=None, nan_policy='omit')]

    def plot_feature(self, feature):
        if feature not in self.branch_features.columns:
            print('Please enter a legit feature name.')
            return
        feat_vals = self.branch_features[feature]
        min_val = np.nanpercentile(feat_vals, 0.5)
        max_val = np.nanpercentile(feat_vals, 99.5)

        # min_val = 1
        # max_val = 2.0

        cmap = mpl.cm.jet
        norm = mpl.colors.Normalize(vmin=min_val, vmax=max_val)

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        cmap = plt.get_cmap('jet')
        for i in range(self.npaths):
            if np.isnan(feat_vals[i]):
                continue
            cur_gen = self.master_df['spline_coords'][i]
            ax.scatter(cur_gen[:,0], cur_gen[:,1], cur_gen[:,2], c=[feat_vals[i]]*len(cur_gen), cmap=cmap, norm=norm)
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, orientation='vertical')
        cbar.set_label(feature)

        # Set labels and title if needed
        ax.set_axis_off()
        ax.set_title(feature)

        plt.show()