function [FV,FV_tot]=extract_gabor(I,I_mask)
[r,c]=size(I);
%[Gabor_filter,Gabor_imgout] = Extract_Gaborfilter_Features(InputImg);

%inputImg can be entire image or ROI
%inputImg should be original image data

maxPixelValue = max(max(I)); % find the maximum

minPixelValue = min(min(I)); % find the minimum

 % make it to the range between 0 to 1 and then multiply by 255.

%I = ((I + minPixelValue)/maxPixelValue)*255;



inputImg=I;
if size(inputImg,3) > 1
   gray_input_Img = rgb2gray(inputImg);
else
   gray_input_Img = inputImg;
end
uint8_gray_input_Img=gray_input_Img;


f = [0,2,4,8,16,32]; 
theta = [0,pi/8,pi/4, 3* pi/8, pi/2, 5*pi/8, 3*pi/4, 7*pi/8];

% f = [2,4,8,16,32]; 
% theta = [pi/8,pi/4, 3* pi/8, pi/2, 3*pi/4];

%Gabor_output_image=zeros(r,c,48);
feature_index=0;    feat={};
for f_index = 1:1:size(f,2)
    for theta_index = 1:1:size(theta,2)
        feature_index=feature_index+1;
        feat{feature_index}=[f(1,f_index),theta(1,theta_index)];
        [G_F,G_I] = GaborFilter(uint8_gray_input_Img,2,4,f(1,f_index),theta(1,theta_index)); 
        Gabor_output_image{1,feature_index}=G_I;
    end
end
FV_tot=Gabor_output_image;



[r, c]=size(I_mask);
FV=[];
fv_con=[];
for i=1:r
    for j=1:c
        fv_con=[];
        if I_mask(i,j)==1
            for k=1:48
                FV_temp=FV_tot{1,k};
                fv=FV_temp(i,j);
                fv_con= [fv_con fv];
            end
        else
            fv_con=[];
        end
        FV=[FV;fv_con];
    end
end



end