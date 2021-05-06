from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import os, sys
import argparse
import re

parser = argparse.ArgumentParser(description='Mask degenerate sites in alignment.')
parser.add_argument("--alignment", type = str, help="sequence(s) to be used, supplied as FASTA files", required=True)
parser.add_argument("--output", type = str, help="output file with masked sequence data.  FASTA file", required=True)

args = parser.parse_args()
    

##  Read sequence alignment
# alignment = SeqIO.parse(args.alignment, "fasta")

##  List of masked SeqRecords
masked_seqs = []

##  Mask sequences
with open (args.alignment, "rU") as aln_handle:
    for record in SeqIO.parse (aln_handle, "fasta"):
        new_seq = str(record.seq.upper())
        new_seq = new_seq.replace("U", "T")
        new_seq_tuple = re.subn('[^ACGTN]', "N", new_seq)
        new_seq = new_seq_tuple[0]
        replacement_count = new_seq_tuple[1]
        
        ##  Create record
        id = record.id
        new_record = SeqRecord(Seq(new_seq), id, "", "")
        
        ##  Add record to list
        masked_seqs.append(new_record)
        
        ##  Write log info
        print (f'seq: {id}\treplacements: {replacement_count}')
    
##  Write output
SeqIO.write(masked_seqs, args.output, "fasta")
    
        
    
    