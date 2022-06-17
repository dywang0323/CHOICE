# CHOICE
This respository is used to record the data analysis processes of CHOICE project, the datasets in this project are mainly composed of metagenomics data and metaproteomics data

# Metagenome

there are 34 subjects from adults and 24 sujects (2 samples for each, 31week and 37 week) from infants (3 samples for most subjects, 2 week, 2 month and 4-5 month)

The process including preprocess, assemly, annotation, binning and statistic analysis
1. Preprocessing the dataset for assembly
 1) Tools/shelf commands
 * merge the datasets based on which person the dataset came from

  cat person1_rep1.fastq person1_replicate2.fastq > person1.fastq

  * preprocessing the datasts, including remove adaptor, triming and error correction

   Tool: bbmap
   
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

  
# Metaproteome
