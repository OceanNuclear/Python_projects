%This script plots the heat map for the orientations across all 129 frames

for k=1:129
	folder='\\ADF\Storage\G\S\GXS465\project\animation\';
	textFilename = sprintf('%dFrameRotationMatrices.txt', k);
	fid		= fopen(fullfile(folder, textFilename), 'rt');
	%Read the dislocation densities data
	textFilename2= sprintf('grainDislocationDensity%d.txt', k);
	fid2		= fopen(fullfile(folder, textFilename2);

% fname='\\ADF\Storage\G\S\GXS465\project\animation\'*n*'FrameRotationMatrices.txt';
% filename = fullfile(fname);% Accesses rotation matrices from text file
% fileID = fopen(filename);				%opens file
formatSpec = '%f';					%speicifies data as floats
sizeA = [3 Inf];					%Sets size of matrix to be extracted from text file
A = fscanf(fid,formatSpec,sizeA);			%extracts matrix
fclose(fid);						%Closes file

sizeDen = [1 Inf];
Den=fscanf(fid2,formatSpec,sizeDen);%* ask bash to output without grain no.
% Den=%*Delete the 1st column
Den = round(Den/(10**10))
fclose(fid2);

A=A';							%Transposes matrix to give a matrix of 3 columns
Den=Den';
if length(Den)!=(length(A)/3): exit()

n = sum(Den) %*Check if this works
B=zeros(n,3);						%Initiates matrix B - where Euler angles are stored

for i=1:n						%Runs loop to generate Euler angles
	if A(i*3,3)==1
		B(i,1)=0;
		B(i,2)=atan(A(3*i-2,2)/A(3*i-2,1))/2;
		B(i,3)=B(i,2);
	else
		B(i,1)=acos(A(i*3,3)); %Phi
		B(i,2)=atan((A(3*i,1)/sin(B(i,1)))/-(A(3*i,2)/sin(B(i,1))));%phi1
		B(i,3)=atan((A(3*i-2,3)/sin(B(i,1)))/(A(3*i-1,3)/sin(B(i,1))));%phi2
	end
end

a='phi1 Phi phi2 phase y x \n';
fid = fopen('Euler.txt','w');
fprintf( fid,a );

for j = 1:size(B,1)
	fprintf(fid,'%g\t',B(j,2),B(j,1),B(j,3),0,0,0);
	fprintf(fid,'\n');
end
fclose(fid);



% Eular and plot
%% Import Script for EBSD Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = {... 
  'notIndexed',...
  crystalSymmetry('cubic', [1 1 1], 'color', 'light blue')};
%% Specify Crystal and Specimen Symmetries
% crystal symmetry
cs = crystalSymmetry('cubic');
% specimen symmetry
ss = specimenSymmetry('mmm');
% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = '\\ADF\Storage\G\S\GXS465\MATLAB\mtex-4.5.2\pole figure';

% which files to be imported
fname = [pname '\Euler.txt'];

%% Import the Data

% create an EBSD variable containing the data
ebsd = loadEBSD(fname,cs,'interface','generic',...
  'ColumnNames', { 'phi1' 'Phi' 'phi2' 'phase' 'x' 'y'}, 'Bunge', 'Radians');

odf = calcODF(ebsd.orientations);
%plotIPDF(ebsd.orientations,[xvector, yvector,zvector],'MarkerSize',3);

plotIPDF(odf,[xvector,yvector, zvector],'antipodal')
mtexColorMap WhiteJet
colorbar;
formatSpec = '%dFrame.jpg';
graphic=sprintf(formatSpec,k);
saveas(gcf,graphic)
end
