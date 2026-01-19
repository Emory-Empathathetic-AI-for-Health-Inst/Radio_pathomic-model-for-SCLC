function [ horz ] = stat_ring(func)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
 horz=[];X1=[]; X2=[]; X3=[]; X4=[]; X5=[]; X6=[];
 k=size(func,2);
for j=1:k
    x11=[];x1=[];x2=[];x3=[];x4=[];x5=[];x6=[];
    x11=func(:,j);
    
    x1=mean(x11);
    x2=median(x11);
    x3=std(x11);
    x4=skewness(x11);
    x5=kurtosis(x11);
    
    X1=horzcat(X1,x1);
    X2=horzcat(X2,x2);
    X3=horzcat(X3,x3);
    X4=horzcat(X4,x4);
    X5=horzcat(X5,x5);
  
end
  horz=horzcat(X1,X2,X3,X4,X5);
end

