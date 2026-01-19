
function I2=find_laplace(I)

I1=I;
I1=double(I1);
I1_filtered = conv2([1 4 6 4 1],[1 4 6 4 1],I1,'same');I1_filtered=I1_filtered/256;
I2=I1-I1_filtered; % level1
I2_filtered = conv2([1 4 6 4 1],[1 4 6 4 1],I2,'same');I2_filtered=I2_filtered/256;
I3=I2-I2_filtered; %level2
I3_filtered = conv2([1 4 6 4 1],[1 4 6 4 1],I3,'same');I3_filtered=I3_filtered/256;
I4=I3-I3_filtered; %level3
end