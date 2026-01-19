function [ ring ] = air_check(label,inter)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
[r,c]=size(inter);
ring=zeros(r,c);
for i=1:r
    for j=1:c
        if ((inter(i,j)==1) && (label(i,j)==1))
            ring(i,j)=1;
        end   
    end
end

end

