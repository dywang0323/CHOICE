# python parse_protein_length.py gff_file output

import os
import sys

gff = sys.argv[1]
output_dir = sys.argv[2]

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

subject = os.path.basename(gff).split("_")[0]
output_file = os.path.join(output_dir, subject + "_protein_length.txt")

with open(gff) as f1_obj, open(output_file, 'w') as fout:
    lines = f1_obj.readlines()

    for line in lines:
        if 'NODE_' in line and 'CDS' in line:
            infors = line.strip().split("\t")
            scaffold = infors[0]
            id_all = infors[8].split(";")[0]
            id_number = id_all.split("_")[1]
            protein = subject + "_" + scaffold + "_" + id_number
            start = int(infors[3])
            end = int(infors[4])
            length = abs(start - end)
            fout.write(protein + "\t" + str(length) + "\n")
