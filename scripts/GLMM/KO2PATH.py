# This script is used for fetching pathway information from KEGG database using the KO number

import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_symbol_and_pathway(ko_number):
    """Fetch the Symbol and Pathway information for a given KO number."""
    url = f"https://www.genome.jp/entry/{ko_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP issues
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Fetch Symbol
        symbol_element = soup.find('th', string='Symbol')
        symbol = symbol_element.find_next_sibling('td').text.strip() if symbol_element else None
        
        # Fetch Pathways including codes and descriptions
        pathway_element = soup.find('th', string='Pathway')
        pathways = []
        # if pathway_element:
        #     pathway_links = pathway_element.find_next_sibling('td').find_all('a')
        #     for link in pathway_links:
        #         map_code = link.text.strip()
        #         # Assuming description follows the link as a sibling text node
        #         description = link.next_sibling.strip() if link.next_sibling else ""
        #         pathways.append(f"{map_code} {description}")
        #     pathway = '; '.join(pathways)
        # else:
        #     pathway = None
        if pathway_element:
            pathway_td = pathway_element.find_next_sibling('td')
            for table in pathway_td.find_all('table'):
                for row in table.find_all('tr'):
                    map_code = row.find('a').text.strip()
                    description = row.find('td').find_next_sibling().text.strip()
                    pathways.append(f"{map_code} {description}")

            pathway = '; '.join(pathways)
        else:
            pathway = None
        
        return symbol, pathway
    except Exception as e:
        print(f"Error fetching data for KO: {ko_number}, error: {e}")
        return None, None

# Load the CSV file into a DataFrame
file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Overall/Infant/GLMM/Annotation/GLMM_Infant_ClusterPro.csv'  # Update this path as needed
df = pd.read_csv(file_path)

# Apply the function to each KO number in the DataFrame
df[['Symbol', 'Pathway']] = pd.DataFrame(df['KO Number'].apply(lambda ko: fetch_symbol_and_pathway(ko) if pd.notnull(ko) else (None, None)).tolist(), index=df.index)

# Adjust columns if necessary (as previously described)
# Ensure 'Annotation' column exists to use as reference for inserting new columns
if 'Annotation' in df.columns:
    cols = df.columns.tolist()
    annotation_index = cols.index('Annotation') + 1
    new_cols_order = cols[:annotation_index + 1] + ['Symbol', 'Pathway'] + [col for col in cols[annotation_index + 1:] if col not in ['Symbol', 'Pathway']]
    df = df[new_cols_order]

# Export the updated DataFrame to a CSV file
export_file_path = '/ourdisk/hpc/prebiotics/dywang/Projects/CHOICE/Metaproteome/Overall/Infant/GLMM/Annotation/GLMM_infant_ClusterPATH.csv'  # Adjust this path as needed
df.to_csv(export_file_path, index=False)

print("DataFrame exported successfully to GLMM_Infant_ClusterPATH.csv.")
