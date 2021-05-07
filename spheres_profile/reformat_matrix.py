import os, sys, json, argparse
from pandas import Series, DataFrame
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser(description='Mask degenerate sites in alignment.')
parser.add_argument("--matrix", type = open, help="JSON formatted input matrix from augur distance", required=True)
parser.add_argument("--output", type = str, help="CSV formatted matrix file", required=True)

args = parser.parse_args()

##  Parse matrix into python data structure    
node_matrix = json.load(args.matrix)



##  Convert matrix to pandas DataFrame
##  Get col/row order
order = node_matrix["nodes"].keys()
matrix_list = []
for seq1 in order:
    distances = Series(node_matrix["nodes"][seq1]["default"])
    ##  Make sure index order is correct
    distances.reindex(index = order)
    matrix_list.append(distances)
    
##  Convert list to DataFrame
matrix_frame = DataFrame(data=matrix_list, index=order)

##  Write to row labelled csv
# matrix_frame.to_csv(path_or_buf = args.output, header = False)

##  Write weighted edge list
# matrix_frame.values[[np.arange(len(matrix_frame))]*2] = np.nan
# matrix_frame.stack().reset_index()
edge_list = matrix_frame.rename_axis('Source')\
  .reset_index()\
  .melt('Source', value_name='Weight', var_name='Target')\
  .query('Source != Target')\
  .reset_index(drop=True)
edge_list.columns = ["ID1", "ID2", "Distance"]
print (edge_list)
edge_list.to_csv(path_or_buf = args.output,index = False)