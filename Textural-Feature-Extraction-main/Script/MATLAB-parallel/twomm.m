function [feats7,feats8,feats9,feats10,feats11,feats12,feats13,feats14,feats15,feats16,feats17,feats18,feats19,feats20,feats21] = twomm(haralick_features,law_features,Gabor_features,collage_features,B_peri,set2)
  
ring7=set2{1,1};
ring8=set2{1,2};
ring9=set2{1,3};
ring10=set2{1,4};
ring11=set2{1,5};
ring12=set2{1,6};
ring13=set2{1,7};
ring14=set2{1,8};
ring15=set2{1,9};
ring16=set2{1,10};
ring17=set2{1,11};
ring18=set2{1,12};
ring19=set2{1,13};
ring20=set2{1,14};
ring21=set2{1,15};

            %Gabor Features
            gabor7=fix_feat(Gabor_features,B_peri,ring7);
            gabor8=fix_feat(Gabor_features,B_peri,ring8);
            gabor9=fix_feat(Gabor_features,B_peri,ring9);
            gabor10=fix_feat(Gabor_features,B_peri,ring10);
            gabor11=fix_feat(Gabor_features,B_peri,ring11);
            gabor12=fix_feat(Gabor_features,B_peri,ring12);
            gabor13=fix_feat(Gabor_features,B_peri,ring13);
            gabor14=fix_feat(Gabor_features,B_peri,ring14);
            gabor15=fix_feat(Gabor_features,B_peri,ring15);
            gabor16=fix_feat(Gabor_features,B_peri,ring16);
            gabor17=fix_feat(Gabor_features,B_peri,ring17);
            gabor18=fix_feat(Gabor_features,B_peri,ring18);
            gabor19=fix_feat(Gabor_features,B_peri,ring19);
            gabor20=fix_feat(Gabor_features,B_peri,ring20);
            gabor21=fix_feat(Gabor_features,B_peri,ring21);
            %Law features
            law7=fix_feat(law_features,B_peri,ring7);
            law8=fix_feat(law_features,B_peri,ring8);
            law9=fix_feat(law_features,B_peri,ring9);
            law10=fix_feat(law_features,B_peri,ring10);
            law11=fix_feat(law_features,B_peri,ring11);
            law12=fix_feat(law_features,B_peri,ring12);
            law13=fix_feat(law_features,B_peri,ring13);
            law14=fix_feat(law_features,B_peri,ring14);
            law15=fix_feat(law_features,B_peri,ring15);
            law16=fix_feat(law_features,B_peri,ring16);
            law17=fix_feat(law_features,B_peri,ring17);
            law18=fix_feat(law_features,B_peri,ring18); 
            law19=fix_feat(law_features,B_peri,ring19);
            law20=fix_feat(law_features,B_peri,ring20);
            law21=fix_feat(law_features,B_peri,ring21);  
            %Haralick features
            haralick7=fix_feat(haralick_features,B_peri,ring7);
            haralick8=fix_feat(haralick_features,B_peri,ring8);
            haralick9=fix_feat(haralick_features,B_peri,ring9);
            haralick10=fix_feat(haralick_features,B_peri,ring10);
            haralick11=fix_feat(haralick_features,B_peri,ring11);
            haralick12=fix_feat(haralick_features,B_peri,ring12);
            haralick13=fix_feat(haralick_features,B_peri,ring13);
            haralick14=fix_feat(haralick_features,B_peri,ring14);
            haralick15=fix_feat(haralick_features,B_peri,ring15);
            haralick16=fix_feat(haralick_features,B_peri,ring16);
            haralick17=fix_feat(haralick_features,B_peri,ring17);
            haralick18=fix_feat(haralick_features,B_peri,ring18);
            haralick19=fix_feat(haralick_features,B_peri,ring19);
            haralick20=fix_feat(haralick_features,B_peri,ring20);
            haralick21=fix_feat(haralick_features,B_peri,ring21);
            %collage features
            collage7=fix_feat(collage_features,B_peri,ring7);
            collage8=fix_feat(collage_features,B_peri,ring8);
            collage9=fix_feat(collage_features,B_peri,ring9);
            collage10=fix_feat(collage_features,B_peri,ring10);
            collage11=fix_feat(collage_features,B_peri,ring11);
            collage12=fix_feat(collage_features,B_peri,ring12);
            collage13=fix_feat(collage_features,B_peri,ring13);
            collage14=fix_feat(collage_features,B_peri,ring14);
            collage15=fix_feat(collage_features,B_peri,ring15);
            collage16=fix_feat(collage_features,B_peri,ring16);
            collage17=fix_feat(collage_features,B_peri,ring17);
            collage18=fix_feat(collage_features,B_peri,ring18);
            collage19=fix_feat(collage_features,B_peri,ring19);
            collage20=fix_feat(collage_features,B_peri,ring20);
            collage21=fix_feat(collage_features,B_peri,ring21);
            
            
            
           feats7=[gabor7,law7,haralick7,collage7];
           feats8=[gabor8,law8,haralick8,collage8];
           feats9=[gabor9,law9,haralick9,collage9];
           feats10=[gabor10,law10,haralick10,collage10];
           feats11=[gabor11,law11,haralick11,collage11];
           feats12=[gabor12,law12,haralick12,collage12];  
           feats13=[gabor13,law13,haralick13,collage13];
           feats14=[gabor14,law14,haralick14,collage14];
           feats15=[gabor15,law15,haralick15,collage15];
           feats16=[gabor16,law16,haralick16,collage16];
           feats17=[gabor17,law17,haralick17,collage17];
           feats18=[gabor18,law18,haralick18,collage18];  
           feats19=[gabor19,law19,haralick19,collage19];
           feats20=[gabor20,law20,haralick20,collage20];
           feats21=[gabor21,law21,haralick21,collage21];   

end

