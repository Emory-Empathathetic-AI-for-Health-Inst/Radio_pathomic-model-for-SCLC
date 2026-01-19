#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 21:23:14 2024

@author: 4o4notfound
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
from scipy.ndimage import convolve1d
import networkx as nx
import os
from scipy.spatial import KDTree
from scipy.interpolate import RegularGridInterpolator
from os.path import join
import pickle
import json

def smooth_spline_interpolate(coordinates, voxel_size, n_mm_apart):
    # Rescale coordinates in millimeters
    rescaled_coordinates = np.multiply(coordinates, voxel_size)
    kernel = np.ones(4) / 4
    rescaled_coordinates = convolve1d(rescaled_coordinates, kernel, mode='nearest', axis=0)
    # Ensure two consecutive points are exactly similar
    unique_rows = []
    for i in range(len(rescaled_coordinates)):
        if i == 0 or not np.array_equal(rescaled_coordinates[i], rescaled_coordinates[i-1]):
            unique_rows.append(rescaled_coordinates[i])
    rescaled_coordinates = np.array(unique_rows)

    # Fit spline
    try:
        tck, u = splprep(rescaled_coordinates.T, u=None, s=0, k=5)
    except:
        tck, u = splprep(rescaled_coordinates.T, u=None, s=0, k=1)            
    u_new = np.linspace(u.min(), u.max(), 3000)

    # Evaluate spline and rescale to original dimensions
    new_coordinates = np.column_stack(splev(u_new, tck))
    new_derivatives = np.column_stack(splev(u_new, tck, der=1))
    norms = np.linalg.norm(new_derivatives, axis=1)
    new_derivatives = new_derivatives / norms[:, np.newaxis]
    
    # Compute cumulative distance and find sampling indices
    dist_diff = new_coordinates[1:] - new_coordinates[:-1]
    distances = np.linalg.norm(dist_diff, axis=1)
    cumulative_distance = np.concatenate(([0], np.cumsum(distances)))
    
    # Determine indices where the distance crosses each n_mm increment
    idx = np.searchsorted(cumulative_distance, np.arange(0, cumulative_distance[-1], n_mm_apart))
    
    return np.divide(new_coordinates[idx], voxel_size), np.divide(new_derivatives[idx], voxel_size)

class qvt:
    def __init__(self, readData, savepath=None, force=True):
        self.Vessels_PT, self.skeleton, self.spacing, self.skanSkel, self.skanSummary, self.edt_image, self.SG, self.savepath = readData.Vessels_PT, readData.skeleton, readData.spacing, readData.skanSkel, readData.skanSummary, readData.edt, readData.SG, readData.outfilepath
        self.initialize_interpolator()
        self.generate_masterdf()
        self.dump_json()
    
    def load(self):
        self.master_df = pd.read_pickle(join(self.savepath, 'master_df.pkl'))
        self.G = pickle.load(open(join(self.savepath, 'graph.pickle'), 'rb'))
        
    def dump_json(self, df=None, path=None):
        if df is None:
            df = self.master_df
        if path is None:
            path = join(self.savepath, 'master_df.pkl')
        df.to_pickle(path)
        pickle.dump(self.G,open(join(self.savepath, 'graph.pickle'), 'wb'))

    def generate_masterdf(self):
        self.cols = ['uid', 'StartPoint', 'EndPoint', 'coords', 'n_coords', 'spline_coords', 'spline_derivative','n_spline_coords', 
                     'edt_values_spline', 'cumulative_distance_bw_points', 'valid']
        self.master_df = pd.DataFrame(columns=self.cols)
        self.master_df.columns = self.cols
        self.npaths = self.skanSkel.n_paths
        self.G = nx.Graph()
        for i in range(self.npaths):
            cur_coords = self.skanSkel.path_coordinates(i)
            spl_coords, der_coords = smooth_spline_interpolate(cur_coords, self.spacing, 0.5)
            
            cur_segdist = self.cumulative_euclidean_distance_between_adjacent_points(spl_coords)
            valid = 1 if len(spl_coords) > 7 else 0
            self.master_df.loc[i] = [i, cur_coords[0], cur_coords[-1], cur_coords, len(cur_coords),
                                     spl_coords, der_coords, len(spl_coords), self.interpolator(spl_coords),
                                     cur_segdist, valid]

            # Add directed edge from start to end for the current branch
            self.G.add_edge(tuple(cur_coords[0]), tuple(cur_coords[-1]), weight=cur_segdist[-1], uid=i)
    
    def cumulative_euclidean_distance_between_adjacent_points(self, coords):
        d = np.multiply(np.diff(coords, axis=0), self.spacing)
        segdists = np.sqrt((d ** 2).sum(axis=1))
        segdists = np.insert(segdists, 0, 0)
        #segdists = np.append(segdists, segdists[-1])
        return np.cumsum(segdists)
    
    def initialize_interpolator(self):
        # Define the coordinate grid for the EDT image
        # Assuming the spacing is 1 unit along each axis
        x_dim, y_dim, z_dim = self.Vessels_PT.shape
        x, y, z = np.arange(x_dim), np.arange(y_dim), np.arange(z_dim)    
        # Create the interpolator function
        self.interpolator = RegularGridInterpolator((x, y, z), self.edt_image, bounds_error=False, fill_value=None)
        
    def plot_region(self, save=False, elev=0, azim=-90):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for i in range(self.npaths):
            ax.scatter(self.master_df.loc[i, 'spline_coords'][:,0], self.master_df.loc[i, 'spline_coords'][:,1], self.master_df.loc[i, 'spline_coords'][:,2])
        ax.view_init(elev=elev, azim=azim)
        plt.axis('off')
        plt.tight_layout()
        if save:
            plt.savefig(join(self.savepath, 'Skeleton.png'))
            plt.close('all')
        else:
            plt.show()

    def plot_graph(self, G=None, ax=None, show_uid=False):
        """Visualizes the graph in 3D using matplotlib."""
        if G is None:
            G = self.G
        pos = {node: node for node in G.nodes()}
    
        # Set up a 3D plotting figure
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
    
        # Draw edges and annotate with weights
        for edge in G.edges():
            x = np.array((pos[edge[0]][0], pos[edge[1]][0]))
            y = np.array((pos[edge[0]][1], pos[edge[1]][1]))
            z = np.array((pos[edge[0]][2], pos[edge[1]][2]))
            ax.plot(x, y, z, color="k")

            # Calculate midpoint for the annotation
            if show_uid:
                mid_x, mid_y, mid_z = (x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2
                uid = G[edge[0]][edge[1]].get('uid', 'nan')  # Default weight to 0 if not specified
                ax.text(mid_x, mid_y, mid_z, str(uid), color="blue")
    
        # Draw nodes
        for node in G.nodes():
            ax.scatter(node[0], node[1], node[2], color="skyblue", s=5)
            # ax.text(node[0], node[1], node[2], s=node, color="red") # This will label the nodes with their coordinates
#        ax.set_xlim(0,512)
#        ax.set_ylim(0,512)
#        ax.set_zlim(0,self.airway.shape[-1])
#        ax.view_init(elev=0, azim=-90)
        ax.view_init(elev=0, azim=-90)
        plt.axis('off')
        plt.show(block=False)
        return ax





