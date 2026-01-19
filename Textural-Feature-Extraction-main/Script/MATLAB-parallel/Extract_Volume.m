function [vol] = Extract_Volume(Mask,PixelDim)

%-- Pixel Dimensions
pdimx=PixelDim(1);
pdimy=PixelDim(2);
pdimz=PixelDim(3);

x = double(Mask);
CC3d = bwconncomp(x);
S3d = regionprops3(CC3d,'volume');
vol = (S3d(1,1).Volume)*pdimx*pdimy*pdimz;




