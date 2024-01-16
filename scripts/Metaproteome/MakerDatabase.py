import os

# Set the directory path containing your .faa files
source_directory_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Maker_aa/'
# Set the directory path for the modified files
output_directory_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Marker_header/'

# Create the output directory if it does not exist
if not os.path.exists(output_directory_path):
    os.makedirs(output_directory_path)

# Loop through all files in the source directory
for filename in os.listdir(source_directory_path):
    if filename.endswith('.faa'):  # Check if the file is a .faa file
        file_path = os.path.join(source_directory_path, filename)
        modified_file_path = os.path.join(output_directory_path, filename)  # Save in the output directory

        # Extract the part of the filename before 'protein'
        file_name_part = filename.split('protein')[0]

        with open(file_path, 'r') as infile, open(modified_file_path, 'w') as outfile:
            for line in infile:
                if line.startswith('>'):
                    outfile.write('>' + file_name_part + line[1:])  # Append the modified file name part to header
                else:
                    outfile.write(line)
