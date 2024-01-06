# CHOICE
This respository is used to record the data analysis processes of CHOICE project, the datasets in this project are mainly composed of metagenomics data and metaproteomics data
## Sample information
There are 34 subjects from adults (2 samples for each, 31week and 37 week)and 24 sujects from infants (3 samples for most subjects, 2 week, 2 month and 4-5 month)
![image](https://github.com/dywang0323/CHOICE/assets/60108209/376e4fc4-2cc1-4ceb-aa73-ffcb8bbd1ce4)

![image](https://github.com/dywang0323/CHOICE/assets/60108209/aa7dd2e9-1647-449b-9c26-495d6e8a198c)


## Metagenome
The process including preprocess, assemly, annotation, binning and statistic analysis
### 1. Preprocessing the dataset

 #### 1). Tools/commands
 Tool: bbtools: https://jgi.doe.gov/data-and-tools/software-tools/bbtools/ 
 * merge the datasets based on which person the dataset came from, and one person as one subject
   ```
   cat person1_rep1.fastq person1_rep2.fastq person1_rep3 > person1.fastq
 * preprocessing the datasts, including remove adaptor, triming and error correction      
  a. remove adaptor
    ```
   bbmap/bbduk.sh in= input.fastq 
   out= output.fastq ktrim=r k=23 mink=11 hdist=1 tpe tbo 
   ref=/bbmap/resources/adapters.fa ftm=5 qtrim=r trimq=10
    ```
   b. triming
   ```
   bbmap/bbduk.sh in=input.fastq 
   out=output.fastq outm=output_m.fastq.gz 
   ref=/bbmap/resources/sequencing_artifacts.fa.gz 
   ref=/bbmap/resources/phix174_ill.ref.fa.gz k=31 hdist=1 stats=stats.txt
    ```   
   c. error correction
   ```
   bbmap/bbnorm.sh in=input.fastq.gz 
   out=output.fastq.gz 
   ecc=t keepall passes=1 bits=16 prefilter
    ```   
   d. decontamination (bbsplit and human genome assembly GRCh38)
   ```
   bbsplit.sh in=subject.fq
   ref=GRCh38.fasta
   basename=out_%.fq
   outu=subject_clean.fastq
   bowtie2-build GRCh38_assembly.fasta
    ```
  ### 2. Assembly 
   
  1). Tool: Metaspades
  https://github.com/ablab/spades
   
  2). Command:
  ```
  metaspades.py --12 subject_interleaved_reads.fq.gz -o subject
  ```
 * Quality control  
   a. calculate the N50 (bbtools)
   ```
   stats.sh in=/subject_scaffold.fasta out=/subject_scaffold
   ```
   b. calculate mapping rate  
   Tool: pullseq, bowtie2 (Bowtie2/2.2.9-intel-2016a) and bbstate  

   Sellect the scaffold with sequence length > 1000bp (pullseq)
   
   ```
   pullseq -i subject_scaffold.fasta -m 1000 > subject_scaffold_min1000.fasta
   ```
   create bowtie2 index file
   ```
   bowtie2-build subject_scaffold_min1000.fasta subject_min1000
   ```
   map reads to the scaffold
   ```
   bowtie2 -x --nounal /subject_min1000 -1 subject_R1.fastq.gz
                                        -2 subject_R2.fastq.gz
                                        -S subject_alignmnent.sam
    ```
   count the number of mapped reads
   ```
   wc -l subject_alignment.sam > subject_alignment.txt
   ``` 
   mapping rate = mapped reads/total reads  (the number of total reads is in the log file of metaspades)

  ### 3. TPM calculation
  1). bowtie2, ruby & shell commad  
  * Count the number of mapped reads  
  ```
  add_read_count.rb subject.sam subject_min1000.fasta > subject.counted
  ```
  * Remove the unwanted information
    ```
    for file in /*.counted; do
    grep -e ">" "$file" > "${file%.counted}.counted.result"
    done
    ```
    ```
    for file in /*.counted.result; do
    sed -i "s/>//g" "$file"
    sed -i "s/read_count_//g" "$file"
    done
    ```
   ### 4. Functional annotation
   1). Tools: kofam_scan  
   https://github.com/takaram/kofam_scan  
   (The official installation instruction is put in the supplementary folder)  
   
   2). Command
   ```
   kofamscan/exec_annotation -o /subject_KO.txt subject_min1000.fasta --tmp-dir subject --cpu 20
   ```
  ### 5. Taxonomic profiling
  1). Tool: MetaPhlAn 4  
      https://github.com/biobakery/MetaPhlAn/wiki/MetaPhlAn-4  
  2). Install and build the database
  ```
  metaphlan --install --bowtie2db /ourdisk/hpc/prebiotics/dywang/Software/Database_meta
  ```
  3). Command:
  ```
  # Define the directory where your datasets are stored
DATASET_DIR="/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/PREPROCESS/Error_correction_B"

# Iterate over the files in the dataset directory
for dataset_file in "$DATASET_DIR"/*.fq.gz; do
    # Get the filename without the directory path and extension
    filename=$(basename "$dataset_file")
    filename_without_extension="${filename%.*}"

    # Decompress the input file if the uncompressed file does not exist
    if [ ! -f "${DATASET_DIR}/${filename_without_extension}.fastq" ]; then
        gunzip -c "$dataset_file" > "${DATASET_DIR}/${filename_without_extension}.fastq"
    fi

    # Run MetaPhlAn on each dataset
    metaphlan -t rel_ab_w_read_stats --add_viruses  "${DATASET_DIR}/${filename_without_extension}.fastq" --input_type fastq -o "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/PREPROCESS/Error_correction_B/${filename_without_extension}.txt" --bowtie2db /ourdisk/hpc/prebiotics/dywang/Software/metaphlan_databases --nproc 30

done
```
### 6. Reactions and pathways profiling
```
model load Python/3.9.6-GCCcore-11.2.0
conda active mpa
humann --input /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/PREPROCESS/EC_B1/CHO56B4to5Month.fq.gz --metaphlan-options "--bowtie2db /ourdisk/hpc/prebiotics/dywang/Software/metaphlan_databases" --output /scratch/dywang/humann/
```
### 7. Binning
1).  tools: metabat, CheckM  
https://bitbucket.org/berkeleylab/metabat/src/master/  
https://github.com/Ecogenomics/CheckM

### 8. Clustering
1). seperate quence name into full length and fractionation:  
* Full length  
```
grep "partial=00" your_dataset.txt > extracted_records.txt
```
* Fraction
```
grep -v "partial=00" your_dataset.txt > extracted_records.txt
```
   
   7. Peptidase annotation
   
   Download the peptidase database from:
   https://www.ebi.ac.uk/merops/download_list.shtml
   
   Convert the .lib into fasta:
   seqkit seq -o protease.fastq /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/protease.lib
   
   seqkit fq2fa protease.fastq -o /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/protease.fasta 
    
# Metaproteome
