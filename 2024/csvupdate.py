import csv

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

# Example usage:
file_path = r'C:\\Users\\Admin\\source\\repos\\bpython_automation\\2024\\renderprogress.csv'
row_index = 4  # Note: row_index is 0-based, so row 3 corresponds to index 2
column_index = 2  # Note: column_index is 0-based, so column 3 corresponds to index 2
new_value = "hello"

change_csv_value(file_path, row_index, column_index, new_value)
