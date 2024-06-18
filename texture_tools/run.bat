setlocal
SET PATH=%PATH%;C:\Program Files\NVIDIA Corporation\NVIDIA Texture Tools
nvtt_export.exe --preset "resizeto2kdds.dpf" --batch "C:\Users\Admin\source\repos\bpython_automation\texture_tools\convertPNGToDDS.nvtt"

echo done
pause