function [FV,law_res] = extract_law(I,I_mask)

law_res = lawsfilter(I);
[r, c] = size(I);
FV = [];
fv_con = [];
for i=1:r
    for j=1:c
        fv_con = [];
        if I_mask(i,j)==1
            for k=1:25
                fv = law_res(i,j,k);
                fv_con = [fv_con fv];
            end
        else
            fv_con = [];
        end
        FV = [FV;fv_con];
    end
end
