import os
import sys

dirName = sys.argv[1] # Get the name of the folder passed to this script
print(f'Creating batch script for directory {dirName}')

filesInDir = os.listdir(dirName) # Get all files in the directory
filesInDir = [f for f in filesInDir if f.lower().endswith('png')] # Get only PNG files
filesInDir = [os.path.join(dirName, f) for f in filesInDir] # Get absolute paths
filesInDir = [f for f in filesInDir if os.path.isfile(f)] # Ignore directories

outScript = open('convertPNGToDDS.nvtt', 'w') # Start a new script

for file in filesInDir:
  newFileName = file.rpartition('.')[0] + '.dds' # Replace .png with .dds
  outScript.write(f'{file} --format bc7 --output {newFileName}\n')

outScript.close()
print('Done')