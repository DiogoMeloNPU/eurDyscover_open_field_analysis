% Source2D values do not exist in Python. So, to work with this information
% in Python it is necessary to create new files in which 'neuron' a
% Sources2D object is unfolded into array like structures that can be
% manipulated in Python. This script performs the described task by
% searching for the original CNFME mat files in the folder
% 'Organized_data_JAS' from GoogleDrive and generates the desired
% simpler/readable .mat file in the respective folder for easy access. Keep
% in mind that for this, you need to have the path of your function
% 'Sources2D_to_simple_mat.m' (as well as 'Sources2D.m') in your MATLAB
% search path.

% Start with a folder and get a list of all subfolders.
% Finds and prints names of all MATLAB files in 
% that folder and all of its subfolders.
clc;    % Clear the command window.
workspace;  % Make sure the workspace panel is showing.
format longg;
format compact;

% Define a starting folder.
start_paths = [fullfile('E:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Organized_data_JAS\D1'), 
               fullfile('E:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Organized_data_JAS\D2')];
           
for dopReceptor = 1:size(start_paths,1)
    % Ask user to confirm or change.
    topLevelFolder = uigetdir(start_paths(dopReceptor, :));
    if topLevelFolder == 0
        return;
    end
    % Get list of all subfolders.
    allSubFolders = genpath(topLevelFolder);
    addpath(allSubFolders); %add the top level folder as well as all subfolders to the MATLAB search path
    % Parse into a cell array.
    remain = allSubFolders;
    listOfFolderNames = {};
    while true
        [singleSubFolder, remain] = strtok(remain, ';');
        if isempty(singleSubFolder)
            break;
        end
        listOfFolderNames = [listOfFolderNames singleSubFolder];
    end
    numberOfFolders = length(listOfFolderNames)

    % Process all image files in those folders.
    for k = 1 : numberOfFolders
        % Get this folder and print it out.
        thisFolder = listOfFolderNames{k};
        fprintf('Processing folder %s\n', thisFolder);

        % Get MATLAB files.
        %dir(thisFolder) %check all the files within each folder
        file_to_process = dir(fullfile(thisFolder, '*.mat'));
        numberOfMatFiles = length(file_to_process)
        % Now we have a list of all files in this folder.

        %when ony one matlab file is found in a specific folder, then I
        %know that file is one I want to process
        if numberOfMatFiles == 1
            name_file_to_process = file_to_process.name
            Sources2D_to_simple_mat(name_file_to_process, thisFolder) 
        end
    end
end
