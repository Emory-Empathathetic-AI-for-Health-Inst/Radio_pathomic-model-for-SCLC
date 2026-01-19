function [new_feat] = fix_feat(feature,label,mask)

[r, c]=size(label);
final={};
feat_size=size(feature,2);
    for k=1:feat_size
    FV_temp=feature(:,k);
    fv_main=zeros(r,c);
    flag1=1;
    for i=1:r
        for j=1:c
            if label(i,j)==1
                fv_main(i,j)=FV_temp(flag1,1);
                flag1=flag1+1;
            end
        end
    end
    final{1,k}= fv_main;   
    end

    
     new_feat=[];
     for k=1:feat_size
     fv=0;flag2=1;
     img=final{1,k};
     for i=1:r
            for j=1:c
                if mask(i,j)==1
                    fv(flag2,1)=img(i,j);
                    flag2=flag2+1;
                end
             end
      end
    new_feat(:,k)=fv;
    end
end

