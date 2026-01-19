function [set1,set2]=computeRing(intra,label,dist)
%where intra is the original label file annotated for the lesion by the expert.
%label is the 30mm peritumoral mask that was intially generated for
%previous experiments. (before annular stuff)
%this function generates the annular bands within a ~30mm region.

dist1=round(5/(dist));
se1= strel('disk',dist1); %looking at 5mm around the tumor
mask1= imdilate(intra,se1);
inter1=mask1-intra;
ring1=air_check(label,inter1); 

dist2=round(10/(dist));
se2= strel('disk',dist2); %looking at 10mm around the tumor
mask2= imdilate(intra,se2);
inter2=mask2-intra;
interp2=inter2-inter1;
ring2=air_check(label,interp2);

dist3=round(15/(dist));
se3= strel('disk',dist3); %looking at 15mm around the tumor
mask3= imdilate(intra,se3);
inter3=mask3-intra;
interp3=inter3-inter2;
ring3=air_check(label,interp3);

dist4=round(20/(dist));
se4= strel('disk',dist4); %looking at 20mm around the tumor
mask4= imdilate(intra,se4);
inter4=mask4-intra;
interp4=inter4-inter3;
ring4=air_check(label,interp4);

dist5=round(25/(dist));
se5= strel('disk',dist5); %looking at 25mm around the tumor
mask5= imdilate(intra,se5);
inter5=mask5-intra;
interp5=inter5-inter4;
ring5=air_check(label,interp5);

dist6=round(30/(dist));
se6= strel('disk',dist6); %looking at 30mm around the tumor
mask6= imdilate(intra,se6);
inter6=mask6-intra;
interp6=inter6-inter5;
ring6=air_check(label,interp6);

set1={ring1,ring2,ring3,ring4,ring5,ring6};

%%

dist7=round(2/(dist));
se7= strel('disk',dist7); %looking at 2mm around the tumor
mask7= imdilate(intra,se7);
inter7=mask7-intra;
ring7=air_check(label,inter7); 

dist8=round(4/(dist));
se8= strel('disk',dist8); %looking at 4mm around the tumor
mask8= imdilate(intra,se8);
inter8=mask8-intra;
interp8=inter8-inter7;
ring8=air_check(label,interp8);

dist9=round(6/(dist));
se9= strel('disk',dist9); %looking at 6mm around the tumor
mask9= imdilate(intra,se9);
inter9=mask9-intra;
interp9=inter9-inter8;
ring9=air_check(label,interp9);

dist10=round(8/(dist));
se10= strel('disk',dist10); %looking at 8mm around the tumor
mask10= imdilate(intra,se10);
inter10=mask10-intra;
interp10=inter10-inter9;
ring10=air_check(label,interp10);

dist11=round(10/(dist));
se11= strel('disk',dist11); %looking at 10mm around the tumor
mask11= imdilate(intra,se11);
inter11=mask11-intra;
interp11=inter11-inter10;
ring11=air_check(label,interp11);

dist12=round(12/(dist));
se12= strel('disk',dist12); %looking at 12mm around the tumor
mask12= imdilate(intra,se12);
inter12=mask12-intra;
interp12=inter12-inter11;
ring12=air_check(label,interp12);

dist13=round(14/(dist));
se13= strel('disk',dist13); %looking at 14mm around the tumor
mask13= imdilate(intra,se13);
inter13=mask13-intra;
interp13=inter13-inter12;
ring13=air_check(label,interp13); 

dist14=round(16/(dist));
se14= strel('disk',dist14); %looking at 16mm around the tumor
mask14= imdilate(intra,se14);
inter14=mask14-intra;
interp14=inter14-inter13;
ring14=air_check(label,interp14);

dist15=round(18/(dist));
se15= strel('disk',dist15); %looking at 18mm around the tumor
mask15= imdilate(intra,se15);
inter15=mask15-intra;
interp15=inter15-inter14;
ring15=air_check(label,interp15);

dist16=round(20/(dist));
se16= strel('disk',dist16); %looking at 20mm around the tumor
mask16= imdilate(intra,se16);
inter16=mask16-intra;
interp16=inter16-inter15;
ring16=air_check(label,interp16);

dist17=round(22/(dist));
se17= strel('disk',dist17); %looking at 22mm around the tumor
mask17= imdilate(intra,se17);
inter17=mask17-intra;
interp17=inter17-inter16;
ring17=air_check(label,interp17);

dist18=round(24/(dist));
se18= strel('disk',dist18); %looking at 24mm around the tumor
mask18= imdilate(intra,se18);
inter18=mask18-intra;
interp18=inter18-inter17;
ring18=air_check(label,interp18);

dist19=round(26/(dist));
se19= strel('disk',dist19); %looking at 26mm around the tumor
mask19= imdilate(intra,se19);
inter19=mask19-intra;
interp19=inter19-inter18;
ring19=air_check(label,interp19);

dist20=round(28/(dist));
se20= strel('disk',dist20); %looking at 28mm around the tumor
mask20= imdilate(intra,se20);
inter20=mask20-intra;
interp20=inter20-inter19;
ring20=air_check(label,interp20);

dist21=round(30/(dist));
se21= strel('disk',dist21); %looking at 30mm around the tumor
mask21= imdilate(intra,se21);
inter21=mask21-intra;
interp21=inter21-inter20;
ring21=air_check(label,interp21);


set2={ring7,ring8,ring9,ring10,ring11,ring12,ring13,ring14,ring15,ring16,ring17,ring18,ring19,ring20,ring21};
end



















