% for Fatemeh XCAT
% gets vector fields from frame by frame coordinate files

function [CoordinateList, VectorField] = ReadVectorField_XCAT(fname)
% fname is vectorfield file e.g. 'A_vec_frame1_to_frame10.txt'

% CoordinateList is list of voxel coordinates [x y z]
% VectorField is list of non-zero vectors [vx vy vz]

fid = fopen(fname);


Xo = []; Yo = []; Zo = []; Xf = []; Zf = []; Yf = []; 


% read that file
while(~feof(fid))
    
    str = fscanf( fid, '%s', 1 );
   
    if strfind(str,'frame')
        % read origin voxel
        x = fscanf( fid,'%f',1);
        y = fscanf( fid,'%f',1);
        z = fscanf( fid,'%f',1);
        
        Xo = [Xo; x];
        Yo = [Yo; y];
        Zo = [Zo; z];
        
        str = fscanf( fid, '%s', 1 );
        
        % read target voxel
        x = fscanf( fid,'%f',1);
        y = fscanf( fid,'%f',1);
        z = fscanf( fid,'%f',1);
        
        Xf = [Xf; (x)];
        Yf = [Yf; (y)];
        Zf = [Zf; (z)];
        
        
    end
end
CoordinateList = [Xo Yo Zo];
VectorField = [Xf-Xo Yf-Yo Zf-Zo];

figure;
quiver3(Yo,Xo,Zo, Yf-Yo,Xf-Xo, Zf-Zo,3)
figure;
quiver(Yo,Xo, Yf-Yo,Xf-Xo,1)

