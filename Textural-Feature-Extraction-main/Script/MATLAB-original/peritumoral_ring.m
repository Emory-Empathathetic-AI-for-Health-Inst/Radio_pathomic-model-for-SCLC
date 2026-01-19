function [ I, B2] = peritumoral_ring(origImage,tumorMask,pix)
%ROI Summary of this function goes here
%   To extract the peritumoral region of a nodule

 se= strel('disk',pix); %change the number of pixels here
 B = imdilate(tumorMask,se);
 B2=B-tumorMask;     
 
%  [r c]=size(origImage);
%  new=zeros(r,c);
%  for i=1:r
%      for j=1:c
%          x=origImage(i,j);
%          if (((-900 <= x) && (x < -100)==1))
%              new(i,j)=origImage(i,j);
%          else
%              new(i,j)=0;
%              B2(i,j)=0;
%          end
%      end
%  end
%  


[r c]=size(origImage);
holes_origImage=zeros(r,c);
 holes_B2=zeros(r,c);
 for i=1:r
     for j=1:c
         x=origImage(i,j);
         if (((-900 <= x) && (x < -100)==1))
             holes_origImage(i,j)=x;
             holes_B2(i,j)=B2(i,j);
         else
             holes_origImage(i,j)= 0;
             holes_B2(i,j)=0;
         end
     end
 end
 
filled_B2=imfill(holes_B2);
B2=zeros(r,c);
B2=logical(filled_B2-tumorMask);
final_origImage=zeros(r,c);
 for i=1:r
     for j=1:c
         if(((B2(i,j)==1) && (holes_B2(i,j)==0)) == 1)
            test=origImage(i-4:i+4,j-4:j+4); %9x9 window
            test=test(test~=origImage(i,j)); %removing center air pixel
            y = mean(test(:)); %calculate average 
            final_origImage(i,j)=y;   
         elseif (((B2(i,j)==1) && (holes_B2(i,j)==1)) == 1)
          final_origImage(i,j)=holes_origImage(i,j); 
         end
     end
 end

    I=zeros(r,c);
    for i=1:r
        for j=1:c
            if (B2(i,j)==1)
            I(i,j)=final_origImage(i,j);  
            end
        end
    end
end


