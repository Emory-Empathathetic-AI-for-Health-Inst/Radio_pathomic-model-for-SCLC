clc;
clear;
% close all;
haralickfun=@haralick2mex;

% before: 3387 seconds
% after: 287 seconds


Files = dir('E:\GT\Research\NLST\Cohort1_T1_Cohort2_T2_resample_thickness\Cohort1_for_feature_extraction');

% add this one
addpath('E:\GT\Research\NLST\feature_extraction');


k=2;

% Initial variables
numFiles = length(Files) - 2; % because every directory has "." and "..", remove it
law_intra = cell(numFiles, 1);
haralick_intra = cell(numFiles, 1);
gabor_intra = cell(numFiles, 1);
intra_file_list = cell(numFiles, 1);

% Start the parallel pool
if isempty(gcp('nocreate'))
    parpool; 
end

tic;
parfor z = 3:length(Files)

    cd('E:\GT\Research\NLST\Cohort1_T1_Cohort2_T2_resample_thickness\Cohort1_for_feature_extraction');
    FileNames = Files(z).name;
    fprintf(2,'\n%s\n',FileNames);
    cd(FileNames);
    V1a = niftiread('CT_T1.nii.gz'); % when read .mha, we can use mha_read_volume.m
    V2a = niftiread('CT_T1-label.nii.gz'); % % when read .mha, we can use mha_read_volume.m

    V1a(:,:,end+1) = 0; % make sure there is no seg in last slice
    V2a(:,:,end+1) = 0; % make sure there is no seg in last slice

    %slices with ROI
    flag1=0;
    first1=0;
    last1=0;

    n=0; %tumor count
    B1=[];L=[];
    for i=1:size(V2a,3)
        B1(:,:)=V2a(:,:,i);
        B1=logical(B1);
        L(:,:) = bwlabel(B1,4);
        X=sum(L(:));
          if (X>0 && flag1==0)
              flag1=1;
              n=n+1;
              first1(n,1)= i;
          end
          if (X==0 && flag1~=0)
              last1(n,1)= i-1;
              flag1=0;
          end 
    end
    B1=[];B=[];
    flag1=1;
    for j=1:n
      for i=first1:last1
          B1(:,:)=V2a(:,:,i);
          B1=double(mat2gray(B1,[0 1])); 
          B(flag1,1)=bwarea(B1);
          B(flag1,2)=i;
          flag1=flag1+1;
      end
    end

        traina_law=[];
%         traina_HU=[];
%         traina_laplace=[];
        traina_haralick=[];
        traina_features=[];
        traina_gabor=[];

        for j=1:n
            if (last1(j) > first1(j)+10)
                for i=first1(j):2:last1(j)
                    Aa = V1a(:,:,i);
                    Aa = double(Aa);
                    Ba = V2a(:,:,i);
                    Ba = logical(Ba);
                    A2a = Aa; B2a=Ba;
                    %Gabor Features
                    fprintf('\nExtracting Gabor..')
                    Gabor_features = extract_gabor(A2a,B2a);
                    traina_gabor = [traina_gabor;Gabor_features];
                    Gabor_features = 0;
                    %Law features
                    fprintf('\nExtracting Law..')
                    law_features = extract_law(A2a,B2a);
                    traina_law = [traina_law;law_features];
                    law_features = 0;
                    %Law-Laplacian features
%                     fprintf('\nExtracting Law-Laplacian..')
%                     laplace_features = find_laplace(A2a);
%                     lawlaplacian_features = extract_law(laplace_features,B2a);
%                     traina_laplace = [traina_laplace;lawlaplacian_features];
%                     laplace_features = 0;
                    %Haralick features
                    fprintf('\nExtracting Haralick..')
                    haralick_features = extract_haralick(A2a,B2a);
                    traina_haralick = [traina_haralick;haralick_features];
                    haralick_features = 0;
                end
            else
                for i=first1(j):last1(j)
                    Aa = V1a(:,:,i);
                    Aa = double(Aa);
                    Ba = V2a(:,:,i);
                    Ba = logical(Ba);
                    A2a = Aa; B2a=Ba;
                    %Gabor Features
                    fprintf('\nExtracting Gabor..')
                    Gabor_features = extract_gabor(A2a,B2a);
                    traina_gabor = [traina_gabor;Gabor_features];
                    Gabor_features = 0;
%                     %HU Features
%                     fprintf('\nExtracting HU..')
%                     HU_features = img(A2a,B2a);
%                     traina_HU = [traina_HU;HU_features];
%                     HU_features = 0;
                    %Law features
                    fprintf('\nExtracting Law..')
                    law_features = extract_law(A2a,B2a);
                    traina_law = [traina_law;law_features];
                    law_features = 0;
                    %Law-Laplacian features
%                     fprintf('\nExtracting Law-Laplacian..')
%                     laplace_features = find_laplace(A2a);
%                     lawlaplacian_features = extract_law(laplace_features,B2a);
%                     traina_laplace = [traina_laplace;lawlaplacian_features];
%                     laplace_features = 0;
                    %Haralick features
                    fprintf('\nExtracting Haralick..')
                    haralick_features = extract_haralick(A2a,B2a);
                    traina_haralick = [traina_haralick;haralick_features];
                    haralick_features = 0;
                end
            end
        end
         
         % Store the result
         law_intra{z-2} = traina_law;
         haralick_intra{z-2} = traina_haralick;
         gabor_intra{z-2} = traina_gabor;
         intra_file_list{z-2} = FileNames;
end
cd('E:\GT\Research\NLST\Cohort1_T1_Cohort2_T2_resample_thickness\Cohort1_intra_peri\intra_feaature')
save('law_intra','law_intra');
%           save('laplace_intra','laplace_intra');
save('haralick_intra','haralick_intra');
save('gabor_intra','gabor_intra');
save('intra_file_list', 'intra_file_list')
toc;
         