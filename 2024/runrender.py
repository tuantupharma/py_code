import os
import csv
import datetime
import time
import signal
import subprocess
import pandas as pd 
# Constants
RENDER_FOLDER = "S:\\rendermanager\\render"
#RENDER_FOLDER = r"C:\\Users\\Admin\\source\\repos\\bpython_automation\\2024" debug
RENDER_SETUP_FILE = "rendersetup.csv"
CSV_FILE = "renderprogress.csv"
BATCH_SIZE = 10

def initialize_render_progress_from_setup():
    render_setup_file = os.path.join(RENDER_FOLDER, RENDER_SETUP_FILE)
    render_progress_file = os.path.join(RENDER_FOLDER, CSV_FILE)

    if not os.path.exists(render_setup_file):
        print("RENDER_SETUP_FILE does not exist.")
        return

    if not os.path.exists(render_progress_file):
        print("renderprogress.csv does not exist. in init")
        create_render_progress_file()
        return

    # Read render setup details from RENDER_SETUP_FILE
    with open(render_setup_file, 'r') as setup_csvfile:
        setup_reader = csv.DictReader(setup_csvfile)
        render_progress_data = []

        for row in setup_reader:
            frame_start = int(row['start_frame'])
            frame_end = int(row['end_frame'])
            computer_name = os.environ['COMPUTERNAME']  # Get computer name

            # Split total frame range into batches of BATCH_SIZE frames
            for batch_start in range(frame_start, frame_end + 1, BATCH_SIZE):
                batch_end = min(batch_start + BATCH_SIZE - 1, frame_end)
                render_progress_data.append({
                    'frame_start': batch_start,
                    'frame_end': batch_end,
                    'status': 'pending',
                    'datetime_begin': datetime.datetime.now(),
                    'complete': 'no',
                    'computer_name': computer_name,
                    'datetime_end': ''
                })
                print(batch_start ," end", batch_end)

    # Update render progress file with initial render progress information
    with open(render_progress_file, 'a', newline='') as progress_csvfile:
        progress_writer = csv.DictWriter(progress_csvfile, fieldnames=render_progress_data[0].keys())
        progress_writer.writerows(render_progress_data)
    
    print("Render progress 1 initialized from setup file.")

    

def create_render_progress_file():
    file_path = os.path.join(RENDER_FOLDER, CSV_FILE)
    if os.path.exists(file_path):
        print("renderprogress.csv already exists.")
        return

    fieldnames = ['frame_start', 'frame_end', 'status', 'datetime_begin', 'complete', 'computer_name']

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    initialize_render_progress_from_setup()
    print("renderprogress.csv created successfully. from create")

# Function to render frames using Blender
def render_frame_range(start_frame, end_frame):
    blender_path = "C:\\blender\\K-Cycles_2023_4.01\\blender.exe"
    blender_file = "\\\\192.168.0.7\\senshu\\DATA\\Natural_scene3\\rendblend\\Cam1_Camera.blend"
    output_render_folder = "S:\\JOBSTUDIO_2022\\data\\natural_scene3\\render"

    # Command to render frames using Blender
    render_command = [
        blender_path,
        "-b", blender_file,  # Run Blender in background mode and specify the file to render
        
        "-s", str(start_frame),  # Start frame
        "-e", str(end_frame),  # End frame
        "-a"  # Render animation
    ]
    
    print(render_command)
    # Execute render command
    try:
        prender = subprocess.Popen(render_command, stdout=None,check=True)
        print(prender)
        print(f"Rendered frames {start_frame} to {end_frame} successfully.")
        time.sleep(15)
        os.kill(p.pid, signal.SIGTERM)
    except subprocess.CalledProcessError as e:
        print(f"Error rendering frames {start_frame} to {end_frame}: {e}")
    time.sleep(15)

def update_csv(frame_start, frame_end, status, computer_name):
    file_exists = os.path.exists(os.path.join(RENDER_FOLDER, CSV_FILE))
    with open(os.path.join(RENDER_FOLDER, CSV_FILE), 'a', newline='') as csvfile:
        fieldnames = ['frame_start', 'frame_end', 'status', 'datetime_begin', 'complete', 'computer_name', 'datetime_end']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({'frame_start': frame_start, 
                         'frame_end': frame_end, 
                         'status': status, 
                         'datetime_begin': datetime.datetime.now(), 
                         'complete': 'no', 
                         'computer_name': computer_name,
                         'datetime_end': ''})

def check_render_progress():
    render_progress_file = os.path.join(RENDER_FOLDER, CSV_FILE)
    if os.path.exists(render_progress_file):
        with open(render_progress_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames or 'status' not in reader.fieldnames:
                print("Invalid render progress file format.")
                return

            all_done = all(row.get('status') == 'done' for row in reader)
            if all_done:
                confirm = input("All frames are rendered. Do you want to recreate renderprogress.csv? (yes/no): ")
                if confirm.lower() == 'yes':
                    os.remove(render_progress_file)
                    print("renderprogress.csv recreated.")
                    #create_render_progress_file()
                    initialize_render_progress_from_setup()
            else:
                print("Not all frames are rendered.")
                return
    else:
        print("renderprogress.csv does not exist.")
        #create_render_progress_file()
        initialize_render_progress_from_setup()
        print("renderprogress.csv created from render progess check")


def read_render_setup():
    render_setup = []
    if not os.path.exists(os.path.join(RENDER_FOLDER, RENDER_SETUP_FILE)):
        print("rendersetup.csv does not exist.")
        print("Let's create render setup details.")

        while True:
            start_frame = input("Enter start frame: ")
            end_frame = input("Enter end frame: ")
            output_format = input("Enter output format: ")
            datetime_value = input("Enter datetime (YYYY-MM-DD HH:MM:SS): ")
            blender_file = input("Enter Blender file name: ")

            render_setup.append({
                'start_frame': start_frame,
                'end_frame': end_frame,
                'output_format': output_format,
                'datetime': datetime_value,
                'blender_file': blender_file
            })

            more_setup = input("Do you want to add more render setup details? (yes/no): ")
            if more_setup.lower() != 'yes':
                break

        # Write render setup to rendersetup.csv
        with open(os.path.join(RENDER_FOLDER, RENDER_SETUP_FILE), 'w', newline='') as csvfile:
            fieldnames = ['start_frame', 'end_frame', 'output_format', 'datetime', 'blender_file']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for setup in render_setup:
                writer.writerow(setup)

    else:
        with open(os.path.join(RENDER_FOLDER, RENDER_SETUP_FILE), 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                render_setup.append(row)

    return render_setup


def change_csv_value(file_path, row_index, column_index, new_value):
    # Read the CSV file and store its contents
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    # Check if the row_index and column_index are within the bounds of the CSV
    if row_index >= len(rows) or column_index >= len(rows[row_index]):
        print("Error: Row or column index out of bounds.")
        return

    # Change the specified value
    rows[row_index][column_index] = new_value

    # Write the updated content back to the CSV file
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
    

    
def main():
    check_render_progress()

    # Check for pending frames and render them
    render_progress_file = os.path.join(RENDER_FOLDER, CSV_FILE)
    if os.path.exists(render_progress_file):
        csvfile = open(render_progress_file, 'r')
        reader = csv.reader(csvfile)
        rows = list(reader)
        dreader= csv.DictReader(csvfile)
        print("begin beforeloop")
        no_lines =0
        for linein in open(render_progress_file, 'r'): 
            no_lines+= 1
        print(no_lines)
        if not dreader:
                print("Invalid render progress file format.")
                return
        line_count = 1
        rowindex = 1
        for rowindex  in range(no_lines):
                
                print(rows[rowindex])
                
                if rows[rowindex][2] != 'pending' or rowindex == 0:
                    print("skip ",rows[rowindex][2],rowindex )
                    continue

                frame_start = int(rows[rowindex][0])
                frame_end = int(rows[rowindex][1])
                computer_name = rows[rowindex][5]
                print("current status :")
                print(rows[rowindex][2])
                # Update status to rendering
                rows[rowindex][2] = 'rendering'
                # Update CSV file
                
                #change_csv_value(file_path, row_index, column_index, new_value)
                change_csv_value(render_progress_file, line_count,2,rows[rowindex][2] )
                change_csv_value(render_progress_file, line_count,4,'complete')
                change_csv_value(render_progress_file, line_count,5,computer_name)
                reader = csv.DictReader(csvfile)
                
                
                # Render frame range
                render_frame_range(frame_start, frame_end)
                
                
                datenow = datetime.datetime.now()
                # Update CSV file
                
                #change_csv_value(file_path, row_index, column_index, new_value)
                change_csv_value(render_progress_file, line_count,2,'done')
                change_csv_value(render_progress_file, line_count,4,'yes')
                change_csv_value(render_progress_file, line_count,6,datenow)
                reader = csv.DictReader(csvfile)
                
                
                line_count += 1
                 
                
                
                

    else:
        print("renderprogress.csv does not exist.")

    
if __name__ == "__main__":
    main()
    
