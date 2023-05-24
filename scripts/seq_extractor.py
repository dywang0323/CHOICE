import sys
from Bio import SeqIO

# Execute by: python seq_extractor.py readsList fastafile outputfile

readsList = open(sys.argv[1], 'rU') # Input interesting sequence IDs, one per line
fastafile = sys.argv[2]             # Input fasta file
outputfile = open(sys.argv[3], 'w') # Output fasta file

wanted = set()
with readsList as f:
    for line in f:
        line = line.strip()
        if line != "":
            wanted.add(line)

fasta_sequences = SeqIO.parse(open(fastafile),'fasta')
with outputfile as i:
    for seq in fasta_sequences:
        if seq.id in wanted:
            SeqIO.write([seq], i, "fasta")

readsList.close()
outputfile.close()
