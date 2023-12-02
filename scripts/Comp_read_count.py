def process_file(input_file, output_file):
    counts = {}

    # Reading the file as a regular text file
    with open(input_file, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            if len(columns) > 1:
                id = columns[1]
                counts[id] = counts.get(id, 0) + 1

    # Writing the output
    with open(output_file, 'w') as out_file:
        for id, count in counts.items():
            out_file.write(f"{id}\t{count}\n")

# Replace with your file paths
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/ReadMapping/MEROPS_B/M8/CHO56B.fq.gz.m8'
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/ReadMapping/MEROPS_B/M8/CHO56B.txt'

process_file(input_file_path, output_file_path)
