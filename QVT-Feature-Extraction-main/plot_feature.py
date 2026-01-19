# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Fri Jan 26 22:06:51 2024
#
# @author: 4o4notfound
# """
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from os.path import join
# import os
# from mayavi import mlab
# import imageio
# import SimpleITK as sitk
# #import matplotlib as mpl
# #import matplotlib.cm as cm
#
#
# class plot_feature:
#     def __init__(self, inpath, feature=None):
#         self.inpath = inpath
#         self.raw_features = pd.read_csv(join(inpath, 'features', 'raw_features.csv'))
#         self.master_df = pd.read_pickle(join(inpath, 'master_df.pkl'))
#         self.features = self.raw_features.columns
#         self.savepath = join(inpath, 'vis')
#         tumves = sitk.ReadImage(join(self.inpath, 'Tumor_Vessels.nii.gz'))
#         tumves = sitk.GetArrayFromImage(tumves).T
#         self.tumor = np.uint8(tumves==1)
#         self.vessels = np.uint8(tumves==2)
#         if feature is not None:
#             self.plot(feature)
#
#     def plot(self, feature, clim=(1, 1.6), save=False):
#         if feature not in self.raw_features.columns:
#             print('Please enter a legit feature name.')
#             return
#
#         feat_df = pd.DataFrame()
#         feat_df[feature] = self.raw_features[feature]
#         feat_df['coords'] = self.master_df['spline_coords']
#
#         if clim is None:
#             min_val = np.nanpercentile(feat_df[feature], 0.5)
#             max_val = np.nanpercentile(feat_df[feature], 99.5)
#             clim = [min_val, max_val]
#         else:
#             min_val = clim[0]
#             max_val = clim[1]
#
#         feat_df_nonans = feat_df[~feat_df[feature].isna()]
#
#         # Create a new figure
#         fig = mlab.figure(feature, size=(1000,800)) # check
#         fig.scene.background = (1, 1, 1) # check
#
# #### START COMMENT - comment this section from START to END if you want to plot the tumor & vessel
#
#         for i in range(len(feat_df_nonans)):
#             coords = feat_df_nonans['coords'].iloc[i]
#             feature_val = feat_df_nonans[feature].iloc[i]
#             x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
#
#             # Points3D for each set of points
#             normalized_val = (feature_val - min_val) / (max_val - min_val)
#             rgba_color = plt.cm.jet(normalized_val)
#             rgb_color = rgba_color[:3]
#             mlab.points3d(x, y, z, color=rgb_color, figure=fig, scale_factor=2)
#             mlab.draw()
#
#         # Create a 3D array with repeated values for the dummy scalar field
#         dummy_data = np.linspace(clim[0], clim[1], 256).reshape((256, 1, 1))
#         dummy = mlab.pipeline.scalar_field(dummy_data)
#
#         # Visualize the dummy field with a module and hide it
#         dummy_module = mlab.pipeline.surface(dummy, colormap='jet')
#         dummy_module.actor.visible = False
#
#         # Set data range for the colorbar
#         dummy_module.module_manager.scalar_lut_manager.use_default_range = False
#         dummy_module.module_manager.scalar_lut_manager.data_range = np.array(clim)
#
#         # Add a colorbar
#         cb = mlab.colorbar(object=dummy_module, title=feature, orientation='vertical')
#         cb.label_text_property.color = (0,0,0)
#         cb.label_text_property.italic = 0
#         cb.title_text_property.italic = 0
#         cb.title_text_property.color = (0,0,0)
#  #### END COMMENT
#         mlab.contour3d(self.tumor, color=(246/255, 210/255, 140/255), figure=fig)   # check
#         mlab.contour3d(self.vessels, color=(215/255, 71/255, 31/255), figure=fig)   # check
#
#         mlab.view(azimuth=90, elevation=90, figure=fig)
#         @mlab.animate(delay=25, ui=True)
#         def rotate():
#             count = 0
#             fig.scene.disable_render = True
#             while 1:
#                 count = count+1
#                 fig.scene.camera.azimuth(1)
#                 fig.scene.render()
#                 if count==361 and save:
#                     print("Screenshots saved. Saving gifs")
#                     fig.scene.movie_maker.record = False
#                     images = []
#                     filenames = os.listdir(join(self.featpath,'movie001'))
#                     for filename in filenames:
#                         images.append(imageio.imread(join(self.featpath,'movie001', filename)))
#                     imageio.mimsave(join(self.savepath,feature+'.gif'), images, loop=0, fps=24)
#                     fig.scene.disable_render = False
#                 yield
#
#         if save:
#             self.featpath = join(self.savepath, feature)
#             os.makedirs(self.featpath, exist_ok=True)
#             fig.scene.movie_maker.directory = self.featpath
#             fig.scene.movie_maker.record = True
#         rotate()
#         mlab.show()
#
#     # def plot(self, feature, clim=None):
#     #     if feature not in self.raw_features.columns:
#     #         print('Please enter a legit feature name.')
#     #         return
#     #     feat_df = pd.DataFrame()
#     #     feat_df[feature] = self.raw_features[feature]
#     #     feat_df['coords'] = self.master_df['spline_coords']
#
#     #     min_val = np.nanpercentile(feat_df[feature], 0.5)
#     #     max_val = np.nanpercentile(feat_df[feature], 99.5)
#
#     #     feat_df_nonans = feat_df[~feat_df[feature].isna()]
#     #     cmap = mpl.cm.jet
#     #     norm = mpl.colors.Normalize(vmin=min_val, vmax=max_val)
#
#     #     c = np.row_stack(feat_df['coords'])
#     #     min_rng = np.min(c, axis=0)
#     #     max_rng = np.max(c, axis=0)
#     #     fig = plt.figure()
#     #     ax = fig.add_subplot(projection='3d')
#     #     cmap = plt.get_cmap('jet')
#     #     trch = self.master_df['spline_coords'][0]
#     #     for i in range(len(feat_df_nonans)):
#     #         cur_gen = feat_df['coords'][i]
#     #         ax.scatter(cur_gen[:,0], cur_gen[:,1], cur_gen[:,2], c=[feat_df[feature][i]]*len(cur_gen), cmap=cmap, norm=norm)
#     #     ax.scatter(trch[:,0], trch[:,1], trch[:,2])
#     #     #ax.view_init(elev=0, azim=-90)
#     #     sm = cm.ScalarMappable(cmap=cmap, norm=norm)
#     #     sm.set_array([])
#     #     if clim is not None:
#     #         sm.set_clim(clim[0], clim[1])
#     #     cbar = plt.colorbar(sm, ax=ax, orientation='vertical')
#     #     cbar.set_label(feature)
#
#     #     ax.set_xlim(min_rng[0], max_rng[0])
#     #     ax.set_ylim(min_rng[1], max_rng[1])
#     #     ax.set_zlim(min_rng[2], max_rng[2])
#     #     # Set labels and title if needed
#     #     ax.set_axis_off()
#     #     ax.set_title(feature)
#
#     #     for angle in range(0, 360):
#     #         # Update the axis view and title
#     #         ax.view_init(elev=0, azim=angle)
#     #         plt.pause(0.0001)
#     #     plt.show()


########## Show the whole lung and tumor_vessel


# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 22:06:51 2024

@author: 4o4notfound
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os.path import join
import os
from mayavi import mlab
import imageio
import SimpleITK as sitk


class plot_feature:
    def __init__(self, inpath, feature=None):
        self.inpath = inpath
        self.raw_features = pd.read_csv(join(inpath, 'features', 'raw_features.csv'))
        self.master_df = pd.read_pickle(join(inpath, 'master_df.pkl'))
        self.features = self.raw_features.columns
        self.savepath = join(inpath, 'vis')
        tumves = sitk.ReadImage(join(self.inpath, 'Tumor_Vessels.nii.gz'))
        tumves = sitk.GetArrayFromImage(tumves).T
        self.tumor = np.uint8(tumves == 1)
        self.vessels = np.uint8(tumves == 2)
        vessels_img = sitk.ReadImage(join(self.inpath, 'Vessels.nii.gz'))
        self.lung_vessels = sitk.GetArrayFromImage(vessels_img).T
        skeleton_img = sitk.ReadImage(join(self.inpath, 'Skeleton.nii.gz'))
        self.skeleton = sitk.GetArrayFromImage(skeleton_img).T
        if feature is not None:
            self.plot(feature)

    def plot(self, feature, clim=(1, 1.6), save=False):
        if feature not in self.raw_features.columns:
            print('Please enter a legit feature name.')
            return

        feat_df = pd.DataFrame()
        feat_df[feature] = self.raw_features[feature]
        feat_df['coords'] = self.master_df['spline_coords']

        if clim is None:
            min_val = np.nanpercentile(feat_df[feature], 0.5)
            max_val = np.nanpercentile(feat_df[feature], 99.5)
            clim = [min_val, max_val]
        else:
            min_val = clim[0]
            max_val = clim[1]

        feat_df_nonans = feat_df[~feat_df[feature].isna()]

        # Create a new figure
        fig = mlab.figure(feature, size=(1000, 800))
        fig.scene.background = (1, 1, 1)

        for i in range(len(feat_df_nonans)):
            coords = feat_df_nonans['coords'].iloc[i]
            feature_val = feat_df_nonans[feature].iloc[i]
            x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]

            # Points3D for each set of points
            normalized_val = (feature_val - min_val) / (max_val - min_val)
            rgba_color = plt.cm.jet(normalized_val)
            rgb_color = rgba_color[:3]
            mlab.points3d(x, y, z, color=rgb_color, figure=fig, scale_factor=2)
            mlab.draw()

        # Create a 3D array with repeated values for the dummy scalar field
        dummy_data = np.linspace(clim[0], clim[1], 256).reshape((256, 1, 1))
        dummy = mlab.pipeline.scalar_field(dummy_data)

        # Visualize the dummy field with a module and hide it
        dummy_module = mlab.pipeline.surface(dummy, colormap='jet')
        dummy_module.actor.visible = False

        # Set data range for the colorbar
        dummy_module.module_manager.scalar_lut_manager.use_default_range = False
        dummy_module.module_manager.scalar_lut_manager.data_range = np.array(clim)

        # Add a colorbar
        cb = mlab.colorbar(object=dummy_module, title=feature, orientation='vertical')
        cb.label_text_property.color = (0, 0, 0)
        cb.label_text_property.italic = 0
        cb.title_text_property.italic = 0
        cb.title_text_property.color = (0, 0, 0)

        # Plot the tumor and lung vessels
        mlab.contour3d(self.tumor, color=(246 / 255, 210 / 255, 140 / 255), figure=fig)
        mlab.contour3d(self.lung_vessels, color=(215 / 255, 71 / 255, 31 / 255), opacity=0.2, figure=fig)

        # Plot the vessel skeleton
        x, y, z = np.where(self.skeleton)
        mlab.points3d(x, y, z, color=(0, 0, 0), mode='cube', scale_factor=1, figure=fig)

        mlab.view(azimuth=90, elevation=90, figure=fig)

        @mlab.animate(delay=25, ui=True)
        def rotate():
            count = 0
            fig.scene.disable_render = True
            while 1:
                count = count + 1
                fig.scene.camera.azimuth(1)
                fig.scene.render()
                if count == 361 and save:
                    print("Screenshots saved. Saving gifs")
                    fig.scene.movie_maker.record = False
                    images = []
                    filenames = os.listdir(join(self.featpath, 'movie001'))
                    for filename in filenames:
                        images.append(imageio.imread(join(self.featpath, 'movie001', filename)))
                    imageio.mimsave(join(self.savepath, feature + '.gif'), images, loop=0, fps=24)
                    fig.scene.disable_render = False
                yield

        if save:
            self.featpath = join(self.savepath, feature)
            os.makedirs(self.featpath, exist_ok=True)
            fig.scene.movie_maker.directory = self.featpath
            fig.scene.movie_maker.record = True
        rotate()
        mlab.show()