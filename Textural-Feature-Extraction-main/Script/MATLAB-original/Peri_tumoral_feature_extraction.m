clc;
clear;
% close all;
haralickfun=@haralick2mex;
% 


Files = dir('E:\GT\Research\CCF\ccf_for_feature_extraction_separate_NIfTI\Adenocarcinoma');

% add this one
addpath('E:\GT\Research\CCF\feature_extraction');

tic;
k=2;

% HU_peri={};
law_peri={};
haralick_peri={};
gabor_peri={};
peri_file_list={}; % save the sequence of processing the CT file. So we can know what each row corresponding each patients
% laplace_peri ={};


for z=3:length(Files)   
    cd('E:\GT\Research\CCF\ccf_for_feature_extraction_separate_NIfTI\Adenocarcinoma');
    FileNames = Files(z).name;
    fprintf(2,'\n%s\n',FileNames);
    cd(FileNames);
    peri_file_list{end+1} = FileNames; % Save the file list
    V1a = niftiread('CT_T0.nii.gz'); % when read .mha, we can use mha_read_volume.m
    V2a = niftiread('CT_T0-label.nii.gz'); % when read .mha, we can use mha_read_volume.m

    % V1a = mha_read_volume('CT_T0.nii.gz');
    % V2a = mha_read_volume('CT_T0-label.nii.gz');
    
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
          if ((X==0 && flag1~=0) || i==size(V2a,3))
              if (i~=size(V2a,3))
                  last1(n,1)= i-1;
                  flag1=0;
              else
                  last1(n,1)= i;
                  flag1=0;
              end
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
        traina_laplace=[];
        traina_haralick=[];
        traina_features=[];
        traina_gabor=[];

        for j=1:n
            for i=first1:last1
              Aa=V1a(:,:,i);
              Aa=double(Aa);
              Ba=V2a(:,:,i);
              Ba=logical(Ba);
              A2a=Aa; B2a=Ba;
              [A2a,B2a]=peritumoral(Aa,Ba);
                    %Gabor Features
                    fprintf('\nExtracting Gabor..')
                    Gabor_features=extract_gabor(A2a,B2a);
                    traina_gabor=[traina_gabor;Gabor_features];
                    Gabor_features=0;
%                     %HU Features
%                     fprintf('\nExtracting HU..')
%                     HU_features=img(A2a,B2a);
%                     traina_HU=[traina_HU;HU_features];
%                     HU_features=0;
                    %Law features
                    fprintf('\nExtracting Law..')
                    law_features=extract_law(A2a,B2a);
                    traina_law=[traina_law;law_features];
                    law_features=0;
                    %Law-Laplacian features
%                     fprintf('\nExtracting Law-Laplacian..')
%                     laplace_features=find_laplace(A2a);
%                     lawlaplacian_features=extract_law(laplace_features,B2a);
%                     traina_laplace=[traina_laplace;lawlaplacian_features];
%                     laplace_features=0;
                    %Haralick features
                    fprintf('\nExtracting Haralick..')
                    haralick_features=extract_haralick(A2a,B2a);
                    traina_haralick=[traina_haralick;haralick_features];
                    haralick_features=0;
            end
        end 
%          HU_peri{z,1}=traina_HU;
         law_peri{z-2,1}=traina_law;
%          laplace_peri{z,1}=traina_laplace;
         haralick_peri{z-2,1}=traina_haralick;
         gabor_peri{z-2,1}=traina_gabor;
         
         cd('E:\GT\Research\CCF\ccf_feature_results_separate\Adenocarcinoma\Peripheral_feature')
    save('law_peri','law_peri');
%     save('laplace_peri','laplace_peri');
    save('haralick_peri','haralick_peri');
    save('gabor_peri','gabor_peri');
    save('peri_file_list', 'peri_file_list');
end
 toc;   

