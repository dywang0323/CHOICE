def filter_fasta_file(input_file, output_file, keywords, encoding='utf-8'):
    # Convert all keywords to lowercase for case-insensitive matching
    lowercase_keywords = [keyword.lower() for keyword in keywords]

    with open(input_file, 'r', encoding=encoding) as infile, open(output_file, 'w', encoding=encoding) as outfile:
        write_sequence = False
        matched_headers = 0
        written_sequences = 0
        for line in infile:
            if line.startswith('>'):  # Header line
                # Convert the line to lowercase for case-insensitive comparison
                lower_line = line.lower()
                write_sequence = any(keyword in lower_line for keyword in lowercase_keywords)
                if write_sequence:
                    matched_headers += 1
                    line = line.replace(" ", "_")  # Replace spaces with underscores only in header
            if write_sequence:
                outfile.write(line)  # Write line as is for sequences
                written_sequences += 1
        
        print(f"Matched Headers: {matched_headers}")
        print(f"Written Sequences: {written_sequences}")

# Example usage - make sure the paths and keywords are correct
input_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/protease.fasta'
output_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Microbes.fasta'
keywords = ["archaea", "bacteria", "Aspergillus clavatus", "Aspergillus flavus", "Aspergillus fumigatus", "Aspergillus niger", "Aspergillus oryzae", "Candida albicans", "Candida dubliniensis", "Candida glabrata", "Cryptococcus gattii", "Cryptococcus neoformans", "Debaryomyces hansenii", "Fusarium graminearum", "Kluyveromyces lactis", "Pichia pastoris", "Saccharomyces cerevisiae", "Scheffersomyces stipitis", "Schizosaccharomyces pombe", "Talaromyces stipitatus", "Theileria annulata", "Yarrowia lipolytica", "Zygosaccharomyces rouxii"]
encoding = 'latin-1'

# Filtering the file
filter_fasta_file(input_file_path, output_file_path, keywords, encoding)
