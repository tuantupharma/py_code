import os
import sys

dirName = sys.argv[1] # Get the name of the folder passed to this script
print(f'Creating batch script for directory {dirName}')

filesInDir = os.listdir(dirName) # Get all files in the directory
filesInDir = [f for f in filesInDir if f.lower().endswith('png')] # Get only PNG files
filesInDir = [os.path.join(dirName, f) for f in filesInDir] # Get absolute paths
filesInDir = [f for f in filesInDir if os.path.isfile(f)] # Ignore directories
nvtt_exportdir = 'C:\\Program Files\\NVIDIA Corporation\\NVIDIA Texture Tools'
outScript = open('convertPNGToDDS.bat', 'w') # Start a new script
preset = "resizeto2kdds.dpf" 
outScript.write(f'setlocal\nSET PATH=%PATH%;{nvtt_exportdir}\n')
                
for file in filesInDir:
  newFileName = file.rpartition('.')[0] + '.dds' # Replace .png with .dds
  #outScript.write(f'{file} --format bc7 --output {newFileName}\n')
  outScript.write('nvtt_export.exe ' f'"{file}" --preset "resizeto2kdds.dpf" --output "{newFileName}"\n')

outScript.close()
print('Done')


