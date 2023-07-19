import glob
import sys
import numpy

clusters_in = sys.argv[1]
output_file = sys.argv[2]
trans_file = sys.argv[3]

def transpose(file_in, file_out):
    matrix = []
    with open(file_in) as ft_obj:
        for l in ft_obj.readlines():
            matrix.append(l.strip().split("\t"))
    ft_obj.close()
    trans = numpy.transpose(matrix)
    
    ft_out = open(file_out, 'w')
    for m in trans:
        ft_out.write("\t".join(map(str, m)) + "\n")
    
    ft_out.close()


def get_subjects(proteins_in_clus):
    protein_list = proteins_in_clus.split(",")
    subject_dic = {}
    for p in protein_list:
        infors = p.split("_")
        subject = infors[0]
        if subject in subject_dic.keys():
            subject_dic[subject].append(p)
        else:
            subject_dic[subject] = [p]
    return subject_dic

def length_dic(subjectID):
    protein_length = {}
    len_dir = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Length_B/"
    len_file = len_dir + subjectID + "_protein_length.txt"
    with open(len_file) as f2_obj:
        for eachl in f2_obj.readlines():
            cols = eachl.strip().split("\t")
            protein_length[cols[0]] = cols[1]
    f2_obj.close()
    return protein_length

def get_sample_counts(sample_file_name, sid):
    counts_dic = {}
    with open(sample_file_name) as f4_obj:
        for reads_line in f4_obj.readlines():
            colls = reads_line.split(" ")
            scaffold_name = sid + "_" + colls[0]
            counts_dic[scaffold_name] = colls[2].split('\n')[0]
    f4_obj.close()
    return counts_dic

subjects = []
with open("/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/ReadCount/Infant/subjects") as f3_obj:
    for x in f3_obj.readlines():
        subjects.append(x.strip())
f3_obj.close()


with open(clusters_in) as f1_obj:
    clus_lines = f1_obj.readlines()
fout = open(output_file, 'w')

# Loop through clusters
for clus in clus_lines[1:]:
    clusters = {}
    sp_clus = clus.strip().split("\t")
    clusID = sp_clus[0]
    proteins = sp_clus[1]
    proteins_each_subject = get_subjects(proteins)
    clusters[clusID] = proteins_each_subject
    
    # Open separate output file for each cluster
    cluster_output_file = f"{clusID}_{output_file}"
    fout_cluster = open(cluster_output_file, 'w')
    fout_cluster.write("clusters\t" + clusID + "\n")
    
    # Loop through subjects
    for a_subject in subjects:
        protein_len = length_dic(a_subject)
        counts_dir = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/ReadCount/Infant/" + a_subject +"/*.txt"
        samples = glob.glob(counts_dir)
        
        for s in samples:
            clus_counts = []
            sample_counts = get_sample_counts(s, a_subject)
            cid_sum = 0
            protein_dic = clusters[clusID]
            
            if a_subject in protein_dic.keys():
                proteins_used = protein_dic[a_subject]
                
                for apro in proteins_used:
                    if apro in protein_len:
                        scaff = "_".join(apro.split("_")[:-1])
                        scaff_len = float(apro.split("_")[4])
                        protein_reads = float(int(sample_counts[scaff]) / scaff_len * int(protein_len[apro]))
                        cid_sum += protein_reads
            
            clus_counts.append(cid_sum)

            sum_clus_counts = sum(clus_counts)            

            if sum_clus_counts == 0:
                sum_clus_counts = "NA"
        # fout_cluster.write(s + "\t" + "\t".join(map(str, clus_counts)) + "\n")
            fout_cluster.write(a_subject + "\t" + s + "\t" + str(sum_clus_counts) + "\n")


    fout_cluster.close()
fout.close()

transpose(output_file, trans_file)
