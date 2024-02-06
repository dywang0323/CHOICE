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
 Tool: bbtools:  
 https://jgi.doe.gov/data-and-tools/software-tools/bbtools/ 
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
    metaphlan -t rel_ab_w_read_stats --add_viruses  "${DATASET_DIR}/${filename_without_extension}.fastq"
                                     --input_type fastq
                                     -o "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/PREPROCESS/Error_correction_B/${filename_without_extension}.txt"
                                     --bowtie2db /ourdisk/hpc/prebiotics/dywang/Software/metaphlan_databases --nproc 30

done
```
### 6. Gene family, reactions and pathways profiling  
1. Tool: Humann  
   https://github.com/biobakery/humann
2. Command:  
```
model load Python/3.9.6-GCCcore-11.2.0
conda active mpa
humann --input /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/PREPROCESS/EC_B1/CHO56B4to5Month.fq.gz
       --metaphlan-options "--bowtie2db /ourdisk/hpc/prebiotics/dywang/Software/metaphlan_databases"
      --output /scratch/dywang/humann/
```
### 7. Binning
1).  tools: metabat, CheckM and gtdbtk  
https://bitbucket.org/berkeleylab/metabat/src/master/  
https://github.com/Ecogenomics/CheckM  
https://ecogenomics.github.io/GTDBTk/index.html   
2). Command:  
* Prepare the input files
```
samtools view -b -S -o /scratch/dywang/LW3_top/LW3_Top.bam
                      /scratch/dywang/LW3_top/LW3_Top.sam
```
```
samtools sort -o /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Bining/Maternal/Maternal.sorted.bam
               /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Bining/Maternal/Maternal.bam
```
* Generate the depth file
```
metabat/jgi_summarize_bam_contig_depths --outputDepth PATH_TO_OUTPUT/CHO56B.txt
                                          PATH_to_BAM/CHO56B.sorted.bam
```
* Binning
```
metabat -i /CHO01B_min1000.fasta
       -o /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Binning/MAGs_0703/CHO01B
      -a /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Binning/Binning_B/Contig_depths/CHO01B.txt -m 2000
```
* Check the quality of MAGs
```
module load Python/3.9.5-GCCcore-10.3.0
checkm lineage_wf -f /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Binning/checkM_0703.txt -t 10 -x fa
                 --pplacer_threads 1 /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Binning/MAGs_0703
                 /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Binning/QC_0703
```
* Taxonomic classifications
```
 module load HMMER/3.2.1-foss-2017b
 module load pplacer/1.1.alpha19
 module load FastANI/1.31-foss-2019b
 module load FastTree/2.1.11-GCCcore-8.3.0
 module load Python/3.9.5-GCCcore-10.3.0

 conda activate gtdbtk-2.1.1
 module load GTDB-Tk/1.3.0-foss-2019b-Python-3.8.2
 module load DendroPy/4.5.2-GCCcore-10.2.0
gtdbtk classify_wf --extension fa --genome_dir /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/Binning/MAGs_HM_0704 --out_dir /ourdisk/hpc/nullspace/dywang/dont_archive/CHOICE/gtdbtk --cpus 40
```
* Removing the duplicate MAGs
  conda activate drep_env
  dRep dereplicate /check
                   -g /duplicate_genome/*.fa
                   -pa 0.9 -sa 0.95 -nc 0.6 --S_algorithm gANI -p 40
```

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
Cluster at 40%, 65% and 90% identity
* 90% identity
```
module load CD-HIT/4.8.1-foss-2018b  
cd-hit -i /min50/Full_length/Full_length.fasta
      -o /min50/Full_length/nr_90_0.9
      -c 0.9 -n 5  -d 0  -g 1 -p 1 -T 35 -M 0 -G 0 -aS 0.9 -aL 0.9
     > /min50/Full_length/nr_90_0.9.log  
cd-hit-2d -i /min50/Full_length/nr_90_0.9 
        -i2 /min50/Fragment/Fragment.fasta 
        -o /min50/Fragment/nr_90_0.9_fragment 
        -c 0.9 -n 5  -d 0  -g 1 -p 1 -T 35 -M 0 -G 0 -aS 0.9 
        > /min50/Fragment/nr_90_0.9_fragment.log  
```
* 65% identity
```
cd-hit -i /min50/Full_length/nr_90_0.9
      -o /min50/Full_length/nr_65_0.9
      -c 0.65 -n 4  -d 0  -g 1 -p 1 -T 35 -M 0 -G 0 -aS 0.9 -aL 0.9
     > /min50/Full_length/nr_65_0.9.log
cd-hit-2d -i /min50/Full_length/nr_65_0.9
        -i2 /min50/Fragment/nr_90_0.9_fragment
        -o /min50/Fragment/nr_65_0.9_fragment -c 0.65 -n 4  -d 0  -g 1 -p 1 -T 40 -M 0 -G 0 -aS 0.9
        > /min50/Fragment/nr_65_0.9_fragment.log
```
* 40% identity
```
cd-hit -i /min50/Full_length/nr_65_0.9
      -o /min50/Full_length/nr_40_0.9
      -c 0.4 -n 2  -d 0  -g 1 -p 1 -T 35 -M 0 -G 0 -aS 0.9 -aL 0.9
      > /min50/Full_length/nr_40_0.9.log
```
* Merge the full-length and fragment clusters in each step
```
/Software/cd-hit-v4.8.1-2019-0228/clstr_merge.pl /min50/Full_length/nr_40_0.9.clstr
                                                /min50/Fragment/nr_40_0.9_fragment.clstr
                                             > /min50/1st_Merge/nr_40_0.9_full_fragment.clstr
```
* Combine clusters at three level
```
/Software/cd-hit-v4.8.1-2019-0228/clstr_rev.pl /nr_90_0.9_full_fragment.clstr
                                              /nr_65_0.9_full_fragment.clstr
                                             /nr_40_0.9_full_fragment.clstr
                                          > /final.clstr
```
* Filter out clusters that appear in fewer than 10 subjects  
  Before filtering, we got 1647743 clusters in maternal samples and 478559 clusters in infant samples
7. Peptidase annotation
   
   Download the peptidase database from:
   https://www.ebi.ac.uk/merops/download_list.shtml
   
   Convert the .lib into fasta:
   seqkit seq -o protease.fastq /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/protease.lib
   
   seqkit fq2fa protease.fastq -o /ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/protease.fasta 
    
# Metaproteome
