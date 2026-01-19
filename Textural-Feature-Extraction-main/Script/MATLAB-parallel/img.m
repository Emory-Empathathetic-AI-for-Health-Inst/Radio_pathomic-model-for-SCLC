function [ final ] = img( A,B )
%IMG Summary of this function goes here
%   Detailed explanation goes here

[r c] = size(A);
HU = zeros(r,c);
for i=1:r
    for j=1:c
        if (B(i,j)==1)
        HU(i,j) = A(i,j);
        end
    end
end
flag=1;final=0;
for i=1:r
    for j=1:c
        if(HU(i,j)~= 0)
            final(flag,1)=HU(i,j);
            flag = flag+1;
        end
    end
end
end

