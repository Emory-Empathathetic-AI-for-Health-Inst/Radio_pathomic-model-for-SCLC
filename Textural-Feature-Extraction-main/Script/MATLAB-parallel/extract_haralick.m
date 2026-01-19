function [FV,volfeats]=extract_haralick(I,I_mask)
haralickfun=@haralick2mex;
vol=double(I);
nharalicks=13;  % Number of Features 
bg=-1;   % Background
ws=5;    % Window Size
hardist=1;   % Distance in a window
harN=64;     % Maximum number of quantization level
volN=round(rescale_range(vol,0,harN-1));   % Quantizing an image
addedfeats=0;  % Feature counter index
cd('E:\GT\Research\NLST\feature_extraction\haralicklibraries')
volfeats(:,:,addedfeats+(1:nharalicks))=haralickfun(volN,harN,ws,hardist,bg);
[r, c]=size(I);
FV=[];
fv_con=[];
for i=1:r
    for j=1:c
        fv_con=[];
        if I_mask(i,j)==1
            for k=1:13
                fv=volfeats(i,j,k);
                fv_con= [fv_con fv];
            end
        else
            fv_con=[];
        end
        FV=[FV;fv_con];
    end
end
