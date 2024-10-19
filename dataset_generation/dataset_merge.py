import os
import json

# Specify the folder containing your JSON files
folder_path = 'Dataset/'

# Initialize an empty list to store merged data
merged_data = []

# Loop through all JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        # Open each JSON file and load the content
        with open(file_path, 'r') as f:
            data = json.load(f)
            merged_data.extend(data)  # Extend the list with the new data

# Specify the path for the output merged JSON file
output_file = os.path.join(folder_path, 'merged_alpaca_new_data.json')

# Write the merged data to a new JSON file
with open(output_file, 'w') as f:
    json.dump(merged_data, f, indent=4)

print(f"All JSON files have been merged into {output_file}")
