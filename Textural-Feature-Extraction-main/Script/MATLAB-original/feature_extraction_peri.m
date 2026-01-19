clc;
clear;
close all;
% adeno - label 1
% adenoma - label 0

%% load data
cd('E:\GT\Research\CCF\ccf_feature_results_separate\Granuloma\Peripheral_feature')
load gabor_peri
load haralick_peri
load law_peri

addpath('E:\GT\Research\CCF\feature_extraction')
%load laplace_intra
% load shape
%%
%TRAINING adeno peritumoral
y=size(gabor_peri,1);
for i=1:y
%extracting gabor
     peri_gabor(i,:) = stat_ring(gabor_peri{i,1});
%extracting law 
     peri_law(i,:) = stat_ring(law_peri{i,1});
%extracting haralick
     peri_haralick(i,:) = stat_ring(haralick_peri{i,1});
end
% shape = cell2mat(shape);
peri = horzcat(peri_gabor,peri_law,peri_haralick);


%%
% load shape
% shape = cell2mat(shape);
% 
% label = zeros(y,1); %should be modified. from 1:54 are zero and from 54:90 are one
% Test = horzcat(intra_final,peri_final,shape);

save('E:\GT\Research\CCF\ccf_feature_results_separate\Granuloma\Peripheral_feature\peri','peri');













