clc;
clear;
addpath('C:\Users\HADI\Desktop\feature_extraction\haralicklibraries');
addpath('C:\Users\HADI\Desktop\feature_extraction')

% V1a = mha_read_volume('CT.mha');
% V2a = mha_read_volume('SG.mha');

V1a = niftiread('Post1.nii.gz');
V2a = niftiread('Post1-label.nii.gz');

% %  isosurface(V2a,0.5)


% for i=1:size(V2a,3)
%     B=(V2a(:,:,i));
%     if sum(sum(B)) ~= 0
%         figure;imagesc(B)
%         break;
%     end
% end

A=(V1a(:,:,247));
B=(V2a(:,:,247));B = logical(B);

% [A,B]=peritumoral(A,B); %if peritumoral region is needed
% figure;imagesc(B)
 
%[~,gab_list] = extract_gabor(A,B);
% [~,law_list] = extract_law(A,B);
% laplace_features = find_laplace(A);
% [~,lawlap_list] = extract_law(laplace_features,B);
[~,hara_list] = extract_haralick(A,B);
      
new = zeros(512,512);
for i=1:512
    for j=1:512
        if B(i,j)==1
            new(i,j) = hara_list(i,j,1); % better for red color
%             new(i,j) = gab_list{1,9}(i,j);
%             new(i,j) = law_list(i,j,2);
        end
    end
end
      
      %fig1
figure; imagesc(new),colormap('jet');colorbar; %vol_feats(i,j,1); 
      %fig2
% figure;  imagesc(new),colormap('hsv') %vol_feats(i,j,3);
%        %fig3
% figure;  imagesc(new),colormap('parula') %new(i,j)=list{1,15}(i,j);



