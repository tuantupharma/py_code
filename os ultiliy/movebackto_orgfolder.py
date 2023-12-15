import os
import shutil

def move_blend_files(log_file_path):
    log_entries = []

    with open(log_file_path, 'r') as log_file:
        # Skip the header line
        next(log_file)

        for line in log_file:
            original_name, new_name = line.strip().split(',')
            original_folder = os.path.dirname(original_name)

            # Check if the modified file exists
            modified_file_path = os.path.join(original_folder, new_name)
            if os.path.exists(modified_file_path):
                # Move the modified file back to its original folder
                shutil.move(modified_file_path, original_name)
                log_entries.append((original_name, new_name))
            else:
                # Log if the modified file doesn't exist
                log_entries.append((original_name, "Not Found"))

    return log_entries

def write_log_after_move(log_entries, log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write("Original Name,New Name\n")
        for entry in log_entries:
            log_file.write(f"{entry[0]},{entry[1]}\n")

# Log file path from the copy operation
copy_log_file_path = r'K:\\tmpb\\log.csv'

# Move blend files back to their original folders
move_log_entries = move_blend_files(copy_log_file_path)

# Write log after move to a CSV file
write_log_after_move(move_log_entries, r'k:\\tmpb\\log_after_move.csv')

print("Blend files moved successfully.")
