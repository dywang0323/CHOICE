for i in *.fq.gz
do

cp Preprocess.batch ${i%.fq.gz}.batch

sed -i "s/MY_INPUT/$i/g" ${i%.fq.gz}.batch

sbatch ${i%.fq.gz}.batch

done
