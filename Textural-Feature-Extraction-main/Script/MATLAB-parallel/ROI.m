function [ Q ] = ROI( origImage, tumorMask )
%ROI Summary of this function goes here
%   Detailed explanation goes here

I=origImage;
mask=tumorMask;

[r c]=find(mask==1);
c_min=min(c);c_max=max(c);r_min=min(r);r_max=max(r);

x1=r_min;
x2=r_max;
y1=c_min;
y2=c_max;

W=mask(x1:x2,y1:y2);
A=I(x1:x2,y1:y2);
Q=A.*W;
imagesc(Q);

% A=[];
% for i=1:r
%     for j=1:c
%         A(i,j)=I(i,j);
%     end
% end
