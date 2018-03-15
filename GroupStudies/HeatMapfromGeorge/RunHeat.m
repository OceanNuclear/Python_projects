for k=120:120
    folder='\\ADF\Storage\G\S\GXS465\project\dislocation\NewModel\NewModel';
    textFilename = sprintf('%dFrameRotationMatrices.txt', k);
    fid          = fopen(fullfile(folder, textFilename), 'rt');
    formatSpec = '%f';                       %speicifies data as floats
    sizeA = [3 Inf];                         %Sets size of matrix to be extracted from text file
    A = fscanf(fid,formatSpec,sizeA);     %extracts matrix
    fclose(fid);                          %Closes file
    A=A';                                    %Transposes matrix to give a matrix of 3 columns
    
    folder='\\ADF\Storage\G\S\GXS465\project\dislocation\NewModel\NewModel';
    textFilename = sprintf('DislocationDensityFrame%dUnaxialNew.txt', k);
    fid          = fopen(fullfile(folder, textFilename), 'rt');
    formatSpec = '%f';                       %speicifies data as floats
    sizeD = [1 Inf];                         %Sets size of matrix to be extracted from text file
    D = fscanf(fid,formatSpec,sizeD);     %extracts matrix
    fclose(fid);                          %Closes file
    D=D'; 

n=length(A)/3;                           % n is the number of matrices
B=zeros(n,4); 
R=zeros(3,3); 
for i=1:n
   
   R(1,1)= A(3*i-2,1); R(1,2)= A(3*i-2,2); R(1,3)=A(3*i-2,3);
   R(2,1)=A(3*i-1,1); R(2,2)= A(3*i-1,2); R(2,3)=A(3*i-1,3); 
   R(3,1)=A(3*i,1); R(3,2)= A(3*i,2); R(3,3)= A(3*i,3);
   
   Z=[0;0;1];
   v = mtimes(R,Z);
   
   B(i,1)=v(1,1);
   B(i,2)=v(2,1);
   B(i,3)=v(3,1); 
   B(i,4)=D(i,1);
end

a='x y z Intensity \n';
fid = fopen('Coords.txt','w');
fprintf(fid,a);

for j = 1:size(B,1)
    fprintf(fid,'%g\t',B(j,1),B(j,2),B(j,3),B(j,4));
    fprintf(fid,'\n');
end
fclose(fid);


%% Import Script for PoleFigure Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = crystalSymmetry('triclinic', [1 1 1]);

% specimen symmetry
SS = specimenSymmetry('1');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = '\\ADF\Storage\G\S\GXS465\MATLAB\mtex-4.5.2\DislocationHeat';

% which files to be imported
fname = [pname '\Coords.txt'];

%% Specify Miller Indice

h = { ...
  Miller(1,0,0,CS),...
  };

%% Import the Data

% create a Pole Figure variable containing the data
pf = loadPoleFigure(fname,h,CS,SS,'interface','generic',...
  'ColumnNames', { 'x' 'y' 'z' 'Intensity'});

odf=calcODF(pf); %convert pole figure

plotIPDF(odf,[xvector,yvector,zvector],'complete');
mtexColorMap WhiteJet
colorbar
% 
% formatSpec = 'Frame%d.png';
% graphic=sprintf(formatSpec,k);
% saveas(gcf,graphic)

end