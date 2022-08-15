# CHOICE
This respository is used to record the data analysis processes of CHOICE project, the datasets in this project are mainly composed of metagenomics data and metaproteomics data

# Metagenome

there are 34 subjects from adults (2 samples for each, 31week and 37 week)and 24 sujects from infants (3 samples for most subjects, 2 week, 2 month and 4-5 month)

The process including preprocess, assemly, annotation, binning and statistic analysis
1. Preprocessing the dataset for assembly

 1). Tools/shell commands
 * merge the datasets based on which person the dataset came from, and one person as one subject

  cat person1_rep1.fastq person1_replicate2.fastq > person1.fastq

  * preprocessing the datasts, including remove adaptor, triming and error correction

   Tool: bbtools 
   https://jgi.doe.gov/data-and-tools/software-tools/bbtools/
   
   a. remove adaptor
   bbmap/bbduk.sh in= input.fastq 
   out= output.fastq ktrim=r k=23 mink=11 hdist=1 tpe tbo 
   ref=/bbmap/resources/adapters.fa ftm=5 qtrim=r trimq=10
   
   b. triming
   bbmap/bbduk.sh in=input.fastq 
   out=output.fastq outm=output_m.fastq.gz 
   ref=/bbmap/resources/sequencing_artifacts.fa.gz 
   ref=/bbmap/resources/phix174_ill.ref.fa.gz k=31 hdist=1 stats=stats.txt
   
   c. error correction
   bbmap/bbnorm.sh in=input.fastq.gz 
   out=output.fastq.gz 
   ecc=t keepall passes=1 bits=16 prefilter
   
   d. decontamination (bbsplit and human genome assembly GRCh38)
   
  $bbsplit.sh in=subject.fq ref=GRCh38.fasta basename=out_%.fq outu=subject_clean.fastq
   
   bowtie2-build GRCh38_assembly.fasta 
   2. Assembly 
   
   1). Tool: Metaspades
   https://github.com/ablab/spades
   
   2). command:
   python /bin/metaspades.py --12 subject_interleaved_reads.fq.gz -o subject
   
   3). quality control: calculate the mapping rate and N50
   
   a. Tool: pullseq, bowtie2 and bbstate
   
   * calculate the N50 (bbtools)
   
   /bbmap/stats.sh in=/subject_scaffold.fasta out=/subject_scaffold
   
   * calculate mapping rate
   
   Sellect the scaffold with sequence length > 1000bp (pullseq)
   
   pullseq -i subject_scaffold.fasta -m 1000 > subject_scaffold_min1000.fasta
   
   create bowtie2 index file
   
   bowtie2-build subject_scaffold_min1000.fasta subject_min1000
   
   map reads to the scaffold
   
   bowtie2 -x --nounal /subject_min1000 -1 subject_eachSRR_1.fastq.gz
                                        -2 subject_eachSRR_2.fastq.gz
                                        -S subject_alignmnent.sam
   
   count the number of mapped reads
   
   wc -l subject_alignment.sam > subject_alignment.txt
   
   mapping rate = mapped reads/total reads  (the number of total reads is in the log file of metaspades)
   
   3. Calculate the RPKM for each scaffold
   
   
   4. Functional Annotation
   
   1). Tools: kofam_scan
   https://github.com/takaram/kofam_scan
   (The official installation instruction is put in the supplementary folder)
   
   5. Binning
   
   
   
   
    
# Metaproteome
