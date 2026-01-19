function [ feats1,feats2,feats3,feats4,feats5,feats6 ] = fivemm(haralick_features,law_features,Gabor_features,collage_features,B_peri,set1)

ring1=set1{1,1};
ring2=set1{1,2};
ring3=set1{1,3};
ring4=set1{1,4};
ring5=set1{1,5};
ring6=set1{1,6};

            %Gabor Features
            gabor1=fix_feat(Gabor_features,B_peri,ring1);
            gabor2=fix_feat(Gabor_features,B_peri,ring2);
            gabor3=fix_feat(Gabor_features,B_peri,ring3);
            gabor4=fix_feat(Gabor_features,B_peri,ring4);
            gabor5=fix_feat(Gabor_features,B_peri,ring5);
            gabor6=fix_feat(Gabor_features,B_peri,ring6);
            %Law features
            law1=fix_feat(law_features,B_peri,ring1);
            law2=fix_feat(law_features,B_peri,ring2);
            law3=fix_feat(law_features,B_peri,ring3);
            law4=fix_feat(law_features,B_peri,ring4);
            law5=fix_feat(law_features,B_peri,ring5);
            law6=fix_feat(law_features,B_peri,ring6);
            %Haralick features
            haralick1=fix_feat(haralick_features,B_peri,ring1);
            haralick2=fix_feat(haralick_features,B_peri,ring2);
            haralick3=fix_feat(haralick_features,B_peri,ring3);
            haralick4=fix_feat(haralick_features,B_peri,ring4);
            haralick5=fix_feat(haralick_features,B_peri,ring5);
            haralick6=fix_feat(haralick_features,B_peri,ring6);
            %Collage_features
            collage1=fix_feat(collage_features,B_peri,ring1);
            collage2=fix_feat(collage_features,B_peri,ring2);
            collage3=fix_feat(collage_features,B_peri,ring3);
            collage4=fix_feat(collage_features,B_peri,ring4);
            collage5=fix_feat(collage_features,B_peri,ring5);
            collage6=fix_feat(collage_features,B_peri,ring6);
            
           feats1=[gabor1,law1,haralick1,collage1];
           feats2=[gabor2,law2,haralick2,collage2];
           feats3=[gabor3,law3,haralick3,collage3];
           feats4=[gabor4,law4,haralick4,collage4];
           feats5=[gabor5,law5,haralick5,collage5];
           feats6=[gabor6,law6,haralick6,collage6];  

end

