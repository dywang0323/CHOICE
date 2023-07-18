# Prepare the culter file (the input in preparing GLMM analysis)
import re
import re

cluster_file = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Infant.clstr"
output_file = "/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metagenome/GLMM/Infant_cluster_protein_2.txt"

with open(cluster_file) as file_object:
    lines = file_object.readlines()

sum_cluster = {}

n = 0
key_term = ''

for line in lines:
    tmp_line = re.sub(r'\.\.\..*$', '', line)
    new_line = re.sub(r',\s+>', '\t', tmp_line)
    groups = new_line.strip().split("\t")
    
    if groups[0] == ">Cluster 0" and n == 0:
        key_term = "Cluster_0"
        sum_cluster[key_term] = []
        n += 1
        
    elif 'Cluster' in groups[0] and n != 0:
        key_term = re.sub(r'\s+', '_', groups[0])  # Change "Cluster 0" format to "Cluster_0" format
        sum_cluster[key_term] = []
        n += 1

    if len(groups) == 3:
        sum_cluster[key_term].append(groups[2])

# Filter out clusters with less than 5 proteins
filtered_clusters = {cluster_id: proteins for cluster_id, proteins in sum_cluster.items() if len(proteins) >= 5}

with open(output_file, 'w') as f:
    f.write("clusterID\tProteins\n")
    for name in sorted(filtered_clusters.keys(), key=lambda x: int(re.search(r'\d+', x).group())):
        cluster_id = re.sub(r'>', '', name)  # Remove the ">" symbol from clusterID
        protein_list = ",".join(filtered_clusters[name])
        f.write(cluster_id + "\t" + protein_list + "\n")

    f.write("There are " + str(len(filtered_clusters)) + " clusters with 5 or more proteins.\n")
