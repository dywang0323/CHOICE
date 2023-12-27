import sys

# File paths from command line arguments
m8_input = sys.argv[1]
output_uniprot_path = sys.argv[2]

# Dictionary for counting occurrences of each UniProt ID
count_uniprot = {}

# Process .m8 input file to count UniProt IDs
with open(m8_input) as m8_obj:
    for each_line in m8_obj:
        mems = each_line.strip().split("\t")
        
        # Check if the line has at least two elements (to avoid IndexError)
        if len(mems) > 1:
            uniprotid = mems[1]  # Extracting the entire second column as the UniProt ID
            count_uniprot[uniprotid] = count_uniprot.get(uniprotid, 0) + 1
        else:
            print(f"Warning: Line format incorrect or missing data - '{each_line.strip()}'")

# Write output file with unique UniProt IDs and their counts
with open(output_uniprot_path, 'w') as output_uniprot_obj:
    output_uniprot_obj.write("uniprot\tCOUNT\n")
    for uniprot_id, count in count_uniprot.items():
        output_uniprot_obj.write(f"{uniprot_id}\t{count}\n")
