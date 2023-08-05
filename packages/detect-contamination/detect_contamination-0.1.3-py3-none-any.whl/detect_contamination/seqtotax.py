import os
import sys
import argparse
import re

#assigns the header of each entry in the fasta file to seq_ids

def generateseqtotaxid(args):

	path_command = subprocess.run('which epost', 
                                    shell=True, 
                                    capture_output=True
                                )

    if (path_command.returncode != 0):
        raise Exception("epost is not installed or initialised")

	if (args.genomes is None):
		raise Exception("Genome file not specified")

	header_cmd = "egrep '>' " + args.genomes
	#print(header_cmd)
	headers = os.popen(header_cmd).read()
	#print(headers)

	seq_ids1 = re.findall("[A-Z][A-Z][0-9]+[.][0-9]+", headers)
	seq_ids2 = re.findall("[A-Z][A-Z][_][0-9]+[.][0-9]+", headers)
	seq_ids = seq_ids1 + seq_ids2

	seq_list = []

	for seq_id in seq_ids:
		#seq_id = seq_id[:-1]
		seq_list.append(seq_id)

	#creates an array of sequence ids that need to be mapped to their taxonomic id
	seq_f = open("seqids.txt", "w")

	for seq_id in seq_list:
		seq_f.write(seq_id + "\n")

	seq_f.close()
	#map each sequence id to their taxonomic id, requires user to install Entrez Direct (EDirect) https://www.ncbi.nlm.nih.gov/books/NBK179288/

	tax_cmd = "cat seqids.txt | epost -db nuccore | esummary -db nuccore | xtract -pattern DocumentSummary -element AccessionVersion,TaxId"
	results = os.popen(tax_cmd).readlines()

	lines = []
	for line in results:
		line = line.split()[0] + "    " + line.split()[1]
		lines.append(line)

	w = open("seqtotax.txt", "w")
	for line in lines:
		w.write(line + "\n")

	w.close()

	return "seqtotax.txt"
