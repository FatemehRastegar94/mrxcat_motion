pdir = pwd;
addpath(genpath(pdir))

[MRX , image]= MRXCAT_CMR_CINE();

figure;imshow3D(squeeze(image(:,:,:,1)))
SaveAsGif('new_code.gif',double(squeeze(image(:,:,:,1))));

%% load the motion vector field 
[fname,~] = uigetfile({'*.txt','text files (*.txt)'});
[CoordinateList, VectorField] = ReadVectorField_XCAT(fname);