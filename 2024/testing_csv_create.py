import csv
import os
import datetime

# Constants
RENDER_FOLDER = r"C:\\Users\\Admin\\source\\repos\\bpython_automation\\2024"
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
        print("renderprogress.csv does not exist.")
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
                    'computer_name': computer_name
                })

    # Update render progress file with initial render progress information
    with open(render_progress_file, 'a', newline='') as progress_csvfile:
        progress_writer = csv.DictWriter(progress_csvfile, fieldnames=render_progress_data[0].keys())
        progress_writer.writerows(render_progress_data)

    print("Render progress initialized from setup file.")

# Example usage
initialize_render_progress_from_setup()
