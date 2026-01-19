clc;
clear;
close all;

Files = dir('E:\Data\Batch2_ReviewedHadi\Post');

shape={};

for z=3:length(Files)
    cd('E:\Data\Batch2_ReviewedHadi\Post');
    FileNames = Files(z).name;
    fprintf(2,'\n%s\n',FileNames);
    cd(FileNames);
    mask = mha_read_volume('label.mha');
    info = mha_read_header('label.mha'); 
    pixeldim = info.PixelDimensions;
    fprintf('\nExtracting Shape..\n')
    shape{z,1} = ExtractShapeFeature(mask,pixeldim);
end
    
cd('Z:\data\TCGA_LUNG_ANNOTATED\features');
    save('shape','shape');

            
            
            