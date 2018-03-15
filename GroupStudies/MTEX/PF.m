%This script plots the disloaction density for a random set of azimuthal
%and polar angles that I have generated




%% Import Script for PoleFigure Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = crystalSymmetry('cubic', [1 1 1]);

% specimen symmetry
SS = specimenSymmetry('1');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = '\\ADF\Storage\G\S\GXS465\project\dislocation';

% which files to be imported
fname = [pname '\dis1.txt'];

%% Specify Miller Indice

h = { ...
  Miller(1,0,0,CS),...
  };

%% Import the Data in Pole figure form 

% create a Pole Figure variable containing the data
pf = loadPoleFigure(fname,h,CS,SS,'interface','generic',...
  'ColumnNames', { 'Polar Angle' 'Azimuth Angle' 'Intensity'}, 'Radians');

odf=calcODF(pf); %convert pole figure

plotIPDF(odf,[xvector, yvector, zvector],'antipodal');
mtexColorMap WhiteJet
colorbar