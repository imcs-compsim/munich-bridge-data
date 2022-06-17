% Alexander Mendler, 2022-06-07 
clear all
close all
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% User inputs
% a) Loading data
Opt.folder_load = 'C:\Users\ga69vop\Desktop\UniBw FLIGHT\01_Raw data'; % Edit the source path

% b) Processing data
Opt.selCol = [2 3:4];       % Index vector to select columns in file, do not select the 1st one
Opt.desFs = 200;            % Define the desired sampling frequency after downsampling
Opt.maxDuration = 30*60;    % [s] - if a record is longer than the specified duration, the processed data will be stored in multiple output files
Opt.swPlotData = 0;         % '0|1' - visualize the time history before saving 

% c) Saving processed data
Opt.folder_save = 'C:\Users\ga69vop\Desktop\UniBw FLIGHT\02_Processed data';% Define folder for processed data
Opt.fn_save = '02_Processed data'; % Define the new filename after processing
Opt.FileType_save = '.csv'; % define the file type '.csv'|'.mat', 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Initialize
addpath(genpath(Opt.folder_load));

% Create cell array 'Fn' with all files to be processed
clear Fn
step = 1;

% Load single file from load test
fn = ['UniBw_2022-03-09_brace01_load'];
Fn{step} = fn;
step = step+1;

% Load a series of short files
for ii=42:43 % edit the file numbers
    fn = ['UniBw_2022-03-11_ref_ambient_',sprintf('%04d',ii)];
    Fn{step} = fn;
    step = step+1;
end   

% Load one very long file and split it into several files with the desired
% duration
fn = ['UniBw_2022-04-11_support_02_ref_ambient'];
Fn{step} = fn;
step = step+1;

% Convert all files in 'Fn'
diary('log.txt'); % write the output of the command window in a text file
exportData(Fn,Opt)

%% =======================================================================%
function exportData(Fn,Opt)
tic
nInputs = size(Fn,2);
step = 1;
for ii = 1:nInputs
    % Load input data    
    fn = Fn{ii};                % file name
    disp(['Progress ',num2str(ii),'/',num2str(nInputs),': ',fn])
    try
        % Initialize
        warning off
        type = '.csv';              % file type
        s = strcat(fn,type);
        Data = readtable(s);
        varNames_all = Data.Properties.VariableNames;
        
        % Selection indices for measurement channels
        t = Data(:,1);
        y = Data(:,Opt.selCol);        
        varNames = varNames_all(Opt.selCol);
        
        dt = etime(datevec(Data{2,1}),datevec(Data{1,1}));
        T = etime(datevec(Data{end,1}),datevec(Data{1,1}));
        Opt.fs = 1/dt;
        
        % Signal Preprocessing
        ya = table2array(y);
        ta = table2array(t);
        [ta,ya] = procData(ta,ya,Opt);
                        
        % Segmenting
        nFiles = floor(T/Opt.maxDuration);
        if nFiles>1
            for nn=1:nFiles
                nSamples = Opt.maxDuration*Opt.desFs;
                ind = (nn-1)*nSamples + (1:nSamples);
                storeResults(ta(ind,:),ya(ind,:),varNames,Opt,step)
                step=step+1;
            end
        else
            storeResults(ta,ya,varNames,Opt,step)
            step=step+1;
        end
    catch
        beep on; beep
        disp('ERROR: file could no be processed')
    end
end
toc
disp('======================')
disp('FINISHED')
disp('======================')
beep on; beep
end
%% =======================================================================%
function [t1,y1] = procData(t,y,Opt)
if Opt.fs/Opt.desFs
    [p,q] = rat(Opt.desFs/Opt.fs);
    if p==1
        y1 = resample(y, p, q);
        t1 = t(1:q:end,1);
    else
        disp('ERROR: Please choose a different downsampling rate.')
        beep on; beep
    end
else
    y1 = y;
end
end
%% =======================================================================%
function storeResults(ta,ya,varNames,Opt,step)
yt = array2table(ya,'VariableNames',varNames);
tt = array2table(ta,'VariableNames',{'Time'});
Data = [tt, yt];

% Save in Matlab file
switch Opt.FileType_save
    case '.mat'
        save([Opt.folder_save,'\',Opt.fn_save,'_',sprintf('%04d',step),'.mat'],'Data')
    case '.csv'
        writetable(Data,[Opt.folder_save,'\',Opt.fn_save,'_',sprintf('%04d',step),'.csv'],'Delimiter','\t');
    case '.xls'
        writetable(Data,[Opt.folder_save,'\',Opt.fn_save,'_',sprintf('%04d',step),'.xls']);
end

% Visualize result
if Opt.swPlotData==1
    nPlots = size(ya,2);
    if nPlots>27
        nCol = 3;
    elseif nPlots>18
        nCol = 3;
    elseif nPlots>9
        nCol = 2;
    else
        nCol = 1;
    end
    figure(1);clf
    for pp=1:nPlots
        subplot(ceil(nPlots/nCol),nCol,pp)
        plot(ta,ya(:,pp),'k-')
        xlim([ta(1) ta(end)])
        xlabel('Time')
        ylabel([string(varNames{1,pp})])
    end
    disp('PAUSED. Please push any button to continue.')
    pause
end
end

