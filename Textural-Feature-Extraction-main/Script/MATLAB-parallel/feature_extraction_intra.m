clc;
clear;
close all;
% adeno - label 1
% adenoma - label 0

%% load data
cd('E:\GT\Research\SCLC\RoswellPark_SCLC\LS_175_intra_peri\intra_feature')
load gabor_intra
load haralick_intra
load law_intra

addpath('E:\GT\Research\NLST\feature_extraction')
%load laplace_intra
% load shape
%%
%TRAINING adeno peritumoral
y=size(gabor_intra,1);
for i=1:y
%extracting gabor
     intra_gabor(i,:) = stat_ring(gabor_intra{i,1});
%extracting law 
     intra_law(i,:) = stat_ring(law_intra{i,1});
%extracting haralick
     intra_haralick(i,:) = stat_ring(haralick_intra{i,1});
end
% shape = cell2mat(shape);
intra = horzcat(intra_gabor,intra_law,intra_haralick);


%%
% load shape
% shape = cell2mat(shape);
% 
% label = zeros(y,1); %should be modified. from 1:54 are zero and from 54:90 are one
% Test = horzcat(intra_final,peri_final,shape);

save('E:\GT\Research\SCLC\RoswellPark_SCLC\LS_175_intra_peri\intra_feature','intra');













