# Prepare the culter file (the input in preparing GLMM analysis)
import re

cluster_file = "Maternal.clstr"
out_cluster = "nr40_0.9FFprotein_family"
out_count = "nr40_0.9FFsubject_count"

f1 = open(out_cluster, 'w')
f2 = open(out_count, 'w')

with open(cluster_file) as file_object:
    lines = file_object.readlines()

sum_cluster = {}
count_subjects = {}

n = 0
key_term = ''

for line in lines:
    tmp_line = re.sub(r'\.\.\..*$', '', line)
    new_line = re.sub(r',\s+>', '\t', tmp_line)
    groups = new_line.strip().split("\t")
    
    if groups[0] == ">Cluster 0" and n == 0:
        key_term = "Cluster_0"
        sum_cluster[key_term] = []
        count_subjects[key_term] = []
        n += 1
        
    elif 'Cluster' in groups[0] and n != 0:
        key_term = re.sub(r'\s+', '_', groups[0])  # Change "Cluster 0" format to "Cluster_0" format
        sum_cluster[key_term] = []
        count_subjects[key_term] = []
        n += 1

    if len(groups) == 3:
        sum_cluster[key_term].append(groups[2])
        mem = groups[2][0:7]
        if mem not in count_subjects[key_term]:
            count_subjects[key_term].append(mem)

f1.write("clusterID\tProteins\n")

for name in sorted(count_subjects.keys(), key=lambda x: int(re.search(r'\d+', x).group())):
    cluster_id = re.sub(r'>', '', name)  # Remove the ">" symbol from clusterID
    f1.write(cluster_id + "\t" + ",".join([str(x) for x in sum_cluster[name]]) + "\n")
    f2.write(name + "\t" + ",".join([str(x) for x in sum_cluster[name]]) + "\n")

f2.write("There are " + str(len(count_subjects)) + " clusters.\n")

f1.close()
f2.close()
