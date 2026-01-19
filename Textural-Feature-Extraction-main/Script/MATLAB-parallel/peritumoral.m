function [I, B2] = peritumoral(origImage, tumorMask)
%ROI Summary of this function goes here
%   To extract the peritumoral region of a nodule

 se= strel('disk',7,0); %looking at 7 pixels around the tumor
 B = imdilate(tumorMask,se);
 B2=B-tumorMask;     
 
 [r,c]=size(origImage);
% 相当于把这个对 original image pixel的筛选给注释掉了
%  new=zeros(r,c);
%  for i=1:r
%      for j=1:c
%          x=origImage(i,j);
%          if (((-3000 <= x) && (x < 1000)==1)) % ((-3000 <= x) && (x < 1000)==1)
%              new(i,j)=origImage(i,j);
%          else
%              new(i,j)=0;
%              B2(i,j)=0;
%          end
%      end
%  end
 
    I=zeros(r,c);
    for i=1:r
        for j=1:c
            if (B2(i,j)==1)
            I(i,j)=origImage(i,j);
            else 
            I(i,j)=0;  
            end
        end
    end
 
end