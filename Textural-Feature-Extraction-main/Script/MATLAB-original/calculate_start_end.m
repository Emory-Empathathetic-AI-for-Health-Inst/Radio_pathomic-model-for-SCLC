function [largest_slice] = calculate_start_end( V2a)

%   slices with ROI

flag1=0;
first1=0;
last1=0;

for i=1:size(V2a,3)
    B1(:,:)=V2a(:,:,i);
    B1=logical(B1);
    L(:,:) = bwlabel(B1,4);
    X=sum(L(:));
      if (X>0 && flag1==0)
          flag1=1;
          first1= i;
      end
      if (X==0 && flag1~=0)
          last1= i-1;
          flag1=0;
      end 
end
B=[];
flag1=1;
  for i=first1:last1
      B1(:,:)=V2a(:,:,i);
      B1=double(mat2gray(B1,[0 1])); 
      B(flag1,1)=bwarea(B1);
      B(flag1,2)=i;
      flag1=flag1+1;
  end

 slice=B(find(B(:,1)==max(B(:,1))),2);
 largest_slice=slice(1,1);
end

