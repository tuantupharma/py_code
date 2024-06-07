import time
import subprocess
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo

def get_vram_usage():
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)  # Change the index if you have multiple GPUs
    info = nvmlDeviceGetMemoryInfo(handle)
    return info.used / 1024 ** 2  # Convert bytes to MB

def check_vram_and_run(script_to_run):
    start_time = time.time()
    i=0
    while time.time() - start_time < 60:  # Run for 1 minute
        vram_usage = get_vram_usage()
        print(f"Current VRAM usage: {vram_usage:.2f} MB")

        if vram_usage <= 3000:  # Check if VRAM usage is not over 3GB
            i = i+1
            
        
        time.sleep(10)  # Wait for 10 seconds before checking again
    if i> 5 :
        print("VRAM usage is below 3GB. Running the script.")
        #subprocess.run(script_to_run, shell=True)
        return  # Exit after running the script
    
    print("VRAM usage did not drop below 3GB within 1 minute.")

# Example usage
script_to_run = "path_to_your_script"  # Replace with the path to the script you want to run
check_vram_and_run(script_to_run)
