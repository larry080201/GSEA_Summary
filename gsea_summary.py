import os
import pandas as pd
from urllib.request import urlopen
from xml.etree import ElementTree as ET

# Define cutoff values
cutoff = ["NES", "NOM.p.val", "FDR.q.val"]
n = 2  # which header for cutoff
cutoff_value = 0.6

# Define header names
header = ["Idx", "GS", "GS DETAILS", "SIZE", "ES", "NES", "NOM p-val", "FDR q-val", "FWER p-val", "RANK AT MAX", "LEADING EDGE"]

# Create an empty dataframe to store the output
output_table = pd.DataFrame(columns=header)

# Get a list of folders
folders = os.listdir()

# Loop through each folder
for folder in folders:
    # Get a list of files in the folder
    if os.path.isdir(folder):
        gs_cat = os.listdir(folder)
    else:
        break
    
    # Loop through each file in the folder
    for file in gs_cat:
        # Get a list of files in the subfolder
        exp = os.listdir(os.path.join(folder, file))
        
        # Filter for HTML files
        htmls = [e for e in exp if e.startswith("gsea_report_for_") and e.endswith(".html")]
        
        # Loop through each HTML file
        for html in htmls:
            # Read the HTML table into a pandas dataframe

            tables = pd.read_html(os.path.join(folder, file, html))
            table = tables[0]
            
            # Rename the column names
            table.columns = header
            table.columns = [col.replace(" ", ".").replace("-", ".") for col in table.columns]
            
            # Convert columns to numeric
            # table.iloc[:, 3:11] = table.iloc[:, 3:11].apply(pd.to_numeric, errors='coerce')
            table.iloc[:, 3:11] = table.iloc[:, 3:11].apply(pd.to_numeric)
            
            # Add additional columns to the table
            table["Collection"] = folder
            table["Exp"] = file.replace(".Gsea", "")
            table["UP"] = html.replace("gsea_report_for_", "").replace(".html", "")
            
            # Filter the table based on the cutoff value
            if n == 1:
                table = table[abs(table[cutoff[n-1]]) > cutoff_value]
            else:
                table = table[table[cutoff[n-1]] < cutoff_value]
            
            # Append the filtered table to the output dataframe
            if not table.empty:
                output_table = pd.concat([output_table, table], axis=0)

# Print the dimensions of the output dataframe and the filtered dataframe for HallMark collection
print(output_table.shape)
print(output_table[output_table["Collection"] == "HallMark"])
