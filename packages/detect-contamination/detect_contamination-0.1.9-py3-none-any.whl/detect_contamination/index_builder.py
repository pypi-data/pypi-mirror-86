import os
import sys
import argparse
from detect_contamination.seqtotax import generateseqtotaxid

def build_index(args):

	if (args.taxonomy_tree is None):
		raise Exception("Genome file not specified")
	if (args.name_table is None):
		raise Exception("Genome file not specified")
	if (args.index_prefix is None):
		raise Exception("index_prefix not specified")

	threads = args.threads
	if (args.conversion_table is None):
	    conv_table = generateseqtotaxid(args)
	else:
		conv_table = args.conversion_table
		
	tax_table = args.taxonomy_tree
	name_table = args.name_table
	ref_seqs = args.genomes
	ref_filename = args.index_prefix

	build_cmd = "centrifuge-build " + "-p " + str(threads) + " --conversion-table " + conv_table + " --taxonomy-tree " + tax_table + " --name-table " + name_table + " " + ref_seqs + " " + ref_filename

	os.popen(build_cmd)