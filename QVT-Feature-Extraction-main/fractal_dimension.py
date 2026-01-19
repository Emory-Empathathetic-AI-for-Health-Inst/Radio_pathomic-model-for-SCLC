#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 02:03:27 2023

@author: 4o4notfound
"""
import numpy as np
import matplotlib.pyplot as plt

def anisotropic_fractal_dimension(array, voxel_spacing=(1, 1, 1), max_box_size=None, min_box_size=1, n_samples=20, n_offsets=0, plot=False):
    """
    Calculates the fractal dimension of a 3D numpy array considering anisotropic voxel spacing.
    
    Args:
        array (np.ndarray): The array to calculate the fractal dimension of.
        voxel_spacing (tuple): A tuple (dx, dy, dz) representing the spacing of the voxels.
        max_box_size (int): The largest box size, given as the power of 2.
        min_box_size (int): The smallest box size, given as the power of 2.
        n_samples (int): Number of scales to measure over.
        n_offsets (int): Number of offsets for the smallest set N(s).
        plot (bool): If True, plots the fractal dimension calculation.
    """
    dx, dy, dz = voxel_spacing
    if max_box_size is None:
        # Adjust max size for the smallest dimension considering voxel spacing
        max_box_size = int(np.floor(np.log2(min(array.shape[i] * voxel_spacing[i] for i in range(3)))))

    scales = np.floor(np.logspace(max_box_size, min_box_size, num=n_samples, base=2))
    scales = np.unique(scales)  # remove duplicates

    locs = np.where(array > 0)
    voxels = np.array([(x * dx, y * dy, z * dz) for x, y, z in zip(*locs)])

    Ns = []
    for scale in scales:
        touched = []
        if n_offsets == 0:
            offsets = [0]
        else:
            offsets = np.linspace(0, scale, n_offsets)
        for offset in offsets:
            bin_edges = [np.arange(0, i * voxel_spacing[idx], scale * voxel_spacing[idx]) for idx, i in enumerate(array.shape)]
            bin_edges = [np.hstack([-offset, x + offset]) for x in bin_edges]
            H1, e = np.histogramdd(voxels, bins=bin_edges)
            touched.append(np.sum(H1 > 0))
        Ns.append(touched)
    Ns = np.array(Ns)

    Ns = Ns.min(axis=1)

    scales = np.array([np.min(scales[Ns == x]) for x in np.unique(Ns)])
    Ns = np.unique(Ns)
    Ns = Ns[Ns > 0]
    scales = scales[:len(Ns)]
    coeffs = np.polyfit(np.log(1 / scales), np.log(Ns), 1)

    if plot:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(np.log(1 / scales), np.log(Ns), c="teal", label="Measured ratios")
        ax.set_ylabel("$\log N(\\epsilon)$")
        ax.set_xlabel("$\log 1/ \\epsilon$")
        fitted_y_vals = np.polyval(coeffs, np.log(1 / scales))
        ax.plot(np.log(1 / scales), fitted_y_vals, "k--", label=f"Fit: {np.round(coeffs[0], 3)}X+{coeffs[1]}")
        ax.legend()

    return coeffs[0]


def fractal_dimension(array, max_box_size = None, min_box_size = 1, n_samples = 20, n_offsets = 0, plot = False):
    """Calculates the fractal dimension of a 3D numpy array.
    
    Args:
        array (np.ndarray): The array to calculate the fractal dimension of.
        max_box_size (int): The largest box size, given as the power of 2 so that
                            2**max_box_size gives the sidelength of the largest box.                     
        min_box_size (int): The smallest box size, given as the power of 2 so that
                            2**min_box_size gives the sidelength of the smallest box.
                            Default value 1.
        n_samples (int): number of scales to measure over.
        n_offsets (int): number of offsets to search over to find the smallest set N(s) to
                       cover  all voxels>0.
        plot (bool): set to true to see the analytical plot of a calculation.
                            
        
    """
    #determine the scales to measure on
    if max_box_size == None:
        #default max size is the largest power of 2 that fits in the smallest dimension of the array:
        max_box_size = int(np.floor(np.log2(np.min(array.shape))))
    elif max_box_size == 1:
        max_box_size = int(np.floor(np.log2(np.min(array.shape)/2)))
    scales = np.floor(np.logspace(max_box_size,min_box_size, num = n_samples, base =2 ))
    scales = np.unique(scales) #remove duplicates that could occur as a result of the floor
    
    #get the locations of all non-zero pixels
    locs = np.where(array > 0)
    if len(np.shape(array)) == 3:
        voxels = np.array([(x,y,z) for x,y,z in zip(*locs)])
    elif len(np.shape(array)) == 2:
        voxels = np.array([(x,y) for x,y in zip(*locs)])
    elif len(np.shape(array)) == 1:
        voxels = np.array([(x) for x in zip(*locs)])
    
    #count the minimum amount of boxes touched
    Ns = []
    #loop over all scales
    for scale in scales:
        touched = []
        if n_offsets == 0:
            offsets = [0]
        else:
            offsets = np.linspace(0, scale, n_offsets)
        #search over all offsets
        for offset in offsets:
            bin_edges = [np.arange(0, i, scale) for i in array.shape]
            bin_edges = [np.hstack([0-offset,x + offset]) for x in bin_edges]
            H1, e = np.histogramdd(voxels, bins = bin_edges)
            touched.append(np.sum(H1>0))
        Ns.append(touched)
    Ns = np.array(Ns)
    
    #From all sets N found, keep the smallest one at each scale
    Ns = Ns.min(axis=1)
   
    
    
    #Only keep scales at which Ns changed
    scales  = np.array([np.min(scales[Ns == x]) for x in np.unique(Ns)])
    
    
    Ns = np.unique(Ns)
    Ns = Ns[Ns > 0]
    scales = scales[:len(Ns)]
    #perform fit
    coeffs = np.polyfit(np.log(1/scales), np.log(Ns),1)
    
    #make plot
    if plot:
        fig, ax = plt.subplots(figsize = (8,6))
        ax.scatter(np.log(1/scales), np.log(np.unique(Ns)), c = "teal", label = "Measured ratios")
        ax.set_ylabel("$\log N(\epsilon)$")
        ax.set_xlabel("$\log 1/ \epsilon$")
        fitted_y_vals = np.polyval(coeffs, np.log(1/scales))
        ax.plot(np.log(1/scales), fitted_y_vals, "k--", label = f"Fit: {np.round(coeffs[0],3)}X+{coeffs[1]}")
        ax.legend();
    return(coeffs[0])