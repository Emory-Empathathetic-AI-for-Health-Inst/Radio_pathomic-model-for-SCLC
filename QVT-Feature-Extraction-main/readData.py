#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 18:41:41 2024

@author: 4o4notfound
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import SimpleITK as sitk
import edt
from os.path import join
import kimimaro
from skimage.measure import label, regionprops
#from lungmask import LMInferer
from scipy import ndimage as ndi
from skan import Skeleton, summarize
from skimage import morphology

class read_data:

    # For single/average nodule
    # def __init__(self, fpath, peritumoral_window=25):
    #     if fpath[-1]=="/":
    #        fpath = fpath[:-1]
    #     self.outfilepath = fpath
    #     self.peritumoral_window = peritumoral_window
    #     self.mpi = self.outfilepath.split("/")[-1]
    #     print('Reading files...')
    #     self.read()

    # For multiple nodule
    def __init__(self, ct_path, nodule_path, peritumoral_window=25):
        self.outfilepath = os.path.dirname(ct_path)
        self.peritumoral_window = peritumoral_window
        self.mpi = self.outfilepath.split("/")[-1]
        print('Reading files...')
        self.read(ct_path, nodule_path)

    def read_image(self, image_path):
        image = sitk.ReadImage(image_path)
        array = sitk.GetArrayFromImage(image).T
        return array, image
    
    def save_sitk(self, array, path):
        img = sitk.GetImageFromArray(array.T)
        img.CopyInformation(self.CT_sitk)
        sitk.WriteImage(img, path)

    def niiname(self, filename):
        return join(self.outfilepath, filename +".nii.gz")

    def savefile(self, filename):
        return join(self.outfilepath, filename)
    
    # def get_lungmask(self):
    #     inferer = LMInferer()
    #     segmentation = inferer.apply(self.CT_sitk)
    #     segmentation = np.uint8(segmentation>0)
    #     lungmask = sitk.GetImageFromArray(segmentation)
    #     lungmask.CopyInformation(self.CT_sitk)
    #     sitk.WriteImage(lungmask, self.niiname("LungMask"))
    #     self.Lung = segmentation.T

# For single nodules/average nodules
#     def read(self):
#         # CT
#         if os.path.isfile(self.savefile("CT.mha")):
#             self.CT, self.CT_sitk = self.read_image(self.savefile("CT.mha"))
#             sitk.WriteImage(self.CT_sitk, self.niiname("CT"))
#         else:
#             # self.CT, self.CT_sitk = self.read_image(self.niiname("CT")) # change the name
#             self.CT, self.CT_sitk = self.read_image(self.niiname("CT"))
#
#         self.spacing = self.CT_sitk.GetSpacing()
#         self.SliceThickness = self.spacing[2]
#         self.vol_spacing = self.spacing[0] * self.spacing[1] * self.spacing[2]
#
#         # SG
#         if os.path.isfile(self.savefile("SG.mha")):
#             self.SG, SG_sitk = self.read_image(self.savefile("SG.mha"))
#             sitk.WriteImage(SG_sitk, self.niiname("SG"))
#         else:
#             # self.SG, _ = self.read_image(self.niiname("SG")) # Change the name
#             self.SG, _ = self.read_image(self.niiname("CT-label"))
#
#         # # Lung Mask
#         # if os.path.isfile(self.niiname("LungMask")):
#         #     self.Lung, _ = self.read_image(self.niiname("LungMask"))
#         # else:
#         #     self.get_lungmask()
#
#         # Vessels
#         if os.path.isfile(self.niiname("Vessels")):
#             self.Vessels, _ = self.read_image(self.niiname("Vessels"))
#             self.Vessels[self.SG == 1] = 0
#         else:
#             self.segment_vessels()
#
#         # Isolated Vessels
#         self.isolate_perinodular_regions()
#         self.save_sitk(self.Vessels_PT, self.niiname('Vessels_PT'))
#         self.save_sitk(self.tum_ves_img, self.niiname('Tumor_Vessels'))
#
#         # Skeleton
#         if os.path.isfile(self.niiname("Skeleton")):
#             self.skeleton, _ = self.read_image(self.niiname("Skeleton"))
#         else:
#             print("Kimimaro Skeletonization")
#             self.kimimaro_skel()
#             self.save_sitk(self.skeleton, self.niiname('Skeleton'))
#
#         # Euclidean Distance Transform
#         self.edt = edt.edt(self.Vessels, anisotropy = self.spacing, black_border=True, order='F')
#         self.save_sitk(self.edt, self.niiname('EDT'))
#
#         print('Skan...')
#         self.skanSkel = Skeleton(self.skeleton, spacing=self.spacing)
#         self.skanSummary = summarize(self.skanSkel)

# For multiple nodules
    def read(self, ct_path, nodule_path):
        # CT
        self.CT, self.CT_sitk = self.read_image(ct_path)
        sitk.WriteImage(self.CT_sitk, self.niiname("CT"))

        self.spacing = self.CT_sitk.GetSpacing()
        self.SliceThickness = self.spacing[2]
        self.vol_spacing = self.spacing[0] * self.spacing[1] * self.spacing[2]

        # SG (Nodule Mask)
        self.SG, _ = self.read_image(nodule_path)

        # Vessels
        if os.path.isfile(self.niiname("Vessels")):
            self.Vessels, _ = self.read_image(self.niiname("Vessels"))
            self.Vessels[self.SG == 1] = 0
        else:
            self.segment_vessels()

        # Isolated Vessels
        self.isolate_perinodular_regions()
        self.save_sitk(self.Vessels_PT, self.niiname('Vessels_PT'))
        self.save_sitk(self.tum_ves_img, self.niiname('Tumor_Vessels'))

        # Skeleton
        if os.path.isfile(self.niiname("Skeleton")):
            self.skeleton, _ = self.read_image(self.niiname("Skeleton"))
        else:
            print("Kimimaro Skeletonization")
            self.kimimaro_skel()
            self.save_sitk(self.skeleton, self.niiname('Skeleton'))

        # Euclidean Distance Transform
        self.edt = edt.edt(self.Vessels, anisotropy=self.spacing, black_border=True, order='F')
        self.save_sitk(self.edt, self.niiname('EDT'))

        print('Skan...')
        self.skanSkel = Skeleton(self.skeleton, spacing=self.spacing)
        self.skanSummary = summarize(self.skanSkel)

    def segment_vessels(self):
        # cmd_ve = 'TotalSegmentator -i ' + self.niiname("CT") + ' -o ' + self.outfilepath + ' --ta lung_vessels' # Change the name
        cmd_ve = 'TotalSegmentator -i ' + self.niiname("CT") + ' -o ' + self.outfilepath + ' --ta lung_vessels'
        os.system(cmd_ve)
        self.Vessels, _ = self.read_image(self.niiname("lung_vessels"))
        self.Vessels[self.SG==1] = 0
        self.save_sitk(self.Vessels, self.niiname('Vessels'))
        os.remove(join(self.outfilepath, self.niiname("lung_vessels")))
        os.remove(join(self.outfilepath, self.niiname("lung_trachea_bronchia")))
    
    def process_ve(self):
        print('Post-processing vessels...')
        sg_img_dilated = ndi.binary_dilation(self.SG, iterations=5)
        self.Vessels[sg_img_dilated==1] = 0
        Vessels_sitk = sitk.GetImageFromArray(self.Vessels.T)
        Vessels_sitk.CopyInformation(self.CT_sitk)
        sitk.WriteImage(Vessels_sitk, self.niiname("lung_vessels"))
    
    def isolate_perinodular_regions(self):
        nodule_cc, num_nodules = label(self.SG, return_num=True)
        r_props = regionprops(nodule_cc)
        segt_shape = self.Vessels.shape
        self.Vessels_PT = np.zeros_like(self.Vessels)
        self.CT_PT = np.zeros_like(self.Vessels)
        self.crop_indices = []
        
        for nod_idx in range(num_nodules):
            bb = r_props[nod_idx].bbox
            crop_dim_0 = [np.int32(np.maximum(0, bb[0] - self.peritumoral_window/self.spacing[0])), np.int32(np.minimum(segt_shape[0], bb[3] + self.peritumoral_window/self.spacing[0]))]
            crop_dim_1 = [np.int32(np.maximum(0, bb[1] - self.peritumoral_window/self.spacing[1])), np.int32(np.minimum(segt_shape[1], bb[4] + self.peritumoral_window/self.spacing[1]))]
            crop_dim_2 = [np.int32(np.maximum(0, bb[2] - self.peritumoral_window/self.spacing[2])), np.int32(np.minimum(segt_shape[2], bb[5] + self.peritumoral_window/self.spacing[2]))]

            self.crop_indices.append([crop_dim_0, crop_dim_1, crop_dim_2])
        
            segv_cur = self.Vessels[crop_dim_0[0]:crop_dim_0[1], crop_dim_1[0]:crop_dim_1[1], crop_dim_2[0]:crop_dim_2[1]]
            self.Vessels_PT[crop_dim_0[0]:crop_dim_0[1], crop_dim_1[0]:crop_dim_1[1], crop_dim_2[0]:crop_dim_2[1]] = morphology.remove_small_objects(segv_cur>0, min_size=50, connectivity=3)
            self.CT_PT[crop_dim_0[0]:crop_dim_0[1], crop_dim_1[0]:crop_dim_1[1], crop_dim_2[0]:crop_dim_2[1]] = self.CT[crop_dim_0[0]:crop_dim_0[1], crop_dim_1[0]:crop_dim_1[1], crop_dim_2[0]:crop_dim_2[1]]

        self.tum_ves_img = self.SG + 2* self.Vessels_PT
    
    def kimimaro_skel(self):
        skels = kimimaro.skeletonize(
          self.Vessels_PT, teasar_params={
            "scale": 1.5, 
            "const": 2, # physical units
            "pdrf_scale": 100000,
            "pdrf_exponent": 4,
            "soma_acceptance_threshold": 3500, # physical units
            "soma_detection_threshold": 750, # physical units
            "soma_invalidation_const": 300, # physical units
            "soma_invalidation_scale": 2,
            "max_paths": None, # default None
          },
          dust_threshold=2, # skip connected components with fewer than this many voxels
          anisotropy=self.spacing, # default True
          fix_branching=True, # default True
          fix_borders=True, # default True
          fill_holes=True, # default False
          fix_avocados=True, # default False
          progress=False, # default False, show progress bar
          parallel=1, # <= 0 all cpu, 1 single process, 2+ multiprocess
          parallel_chunk_size=5, # how many skeletons to process before updating progress bar
        )
        
        skel = kimimaro.postprocess(
          skels[1],
          dust_threshold=4, # physical units
          tick_threshold=4 # physical units
        )
        skel = kimimaro.join_close_components(skel, radius=None)
        
        sk = skel
        #sk = skels[list(skels.keys())[0]].remove_disconnected_vertices()
        
        verts = sk.vertices
        v = np.round(np.divide(verts, self.spacing)).astype(np.int16)
        #v = np.round(verts).astype(np.int16)
        self.skeleton = np.zeros_like(self.Vessels_PT, dtype=np.uint8)
        self.skeleton[v[:,0], v[:,1], v[:,2]] = 1


