# This script is a temporary substitute for the Snakefile.
# It runs blastn, pmlst, and the FishingForPlasmids script.

import sys
import os

workDir = os.getcwd()
assemblyDir = workDir + "/data/assemblyDir/"
blast_dbDir = workDir + "/blast_db/"
pFinderDir = workDir + "/data/blast_pFinder/"
pmlstDir = workDir + "/data/pmlst_out/"
EcPlGeDir = workDir + "/data/blast_EcPlGe/"
FFPDir = workDir + "/data/FFP_output/"

sys.path.append(assemblyDir)
sys.path.append(blast_dbDir)
sys.path.append(pFinderDir)
sys.path.append(pmlstDir)
sys.path.append(EcPlGeDir)
sys.path.append(FFPDir)

configfile = workDir + "/config.YAML"
run_list = []
# open the configfile and read its lines
print(configfile)
try:
    with open(configfile) as conF:
        conFlines = conF.readlines()
except IOError:
    print("cannot open config file: ", configfile)

# obtain a list of sample names to run and to know the file extension of the assembly files
for conFline in conFlines:
    conFline = conFline.rstrip()
    if conFline.startswith("-"):
        sample = conFline.replace("- ", "")
        run_list.extend([sample])
    elif conFline.startswith("file_extension:"):
        file_extension = conFline.split(": ")[1]

for run in run_list:
    assembly_input = assemblyDir + run + "." + file_extension
    pFinder_output = pFinderDir + run + ".csv"
# pFinder_command: runs a blastn with assembly contigs against the plasmid finder database
    pFinder_command = "blastn -query " + assembly_input + " -db " + blast_dbDir + "pFinder_db -out " + pFinder_output + " -num_threads 8 -perc_identity 95 -outfmt '6 qseqid sseqid pident length qcovs qstart qend sstart send evalue bitscore' -max_target_seqs 1 -max_hsps 1"
    print("--START blastn vs plasmid Finder database-- for: ", run)
    os.system(pFinder_command)
    print("--END blastn vs plasmid Finder database-- for: ", run)
    print("Output file: ", pFinder_output)

    pmlstRunDir = pmlstDir + run + "/"
    mkDirPMLSTcommand = "mkdir " + pmlstRunDir
    os.system(mkDirPMLSTcommand) # creating run directory in pmlst_out directory
    pmlst_output = pmlstRunDir + run + ".csv"
# pmlst: runs the function pmlst_script.py, which runs pmlst for specific plasmid types
    from scripts import pmlst_script
    pmlst_script.pmlst(pFinder_output, assembly_input, pmlstRunDir, pmlst_output)

    EcPlGe_output = EcPlGeDir + run + ".csv"
# EcPlGe_command:runs blastn with assembly contigs against a database containing plasmids and E. coli chromosomes
    EcPlGe_command = "blastn -query " + assembly_input + " -db " + blast_dbDir + "EcPlGe_db -out " + EcPlGe_output + " -num_threads 8 -perc_identity 95 -outfmt '6 qseqid sseqid pident length qcovs qstart qend sstart send evalue bitscore' -max_target_seqs 5 -max_hsps 1 -qcov_hsp_perc 20"
    print("--START blastn vs EcPlGe database-- for: ", run)
    os.system(EcPlGe_command)
    print("--END blastn vs EcPlGe database-- for: ", run)
    print("Output file: ", EcPlGe_output)

    FFPrunDir = FFPDir + run + "/"
    mkDirFFPcommand = "mkdir " + FFPrunDir
    os.system(mkDirFFPcommand) # creating run directory in FFP_output directory
    FFP_output = FFPrunDir + run + "_AssignedContigs.csv"
# FishingForPlasmids: runs the FishingForPlasmids function, which uses all output files of the previous tools to generate .fasta files of all plasmids in an assembly
    from scripts import function_FishingForPlasmids2_2
    print("--STARTING FishingForPlasmids-- for file:", run)
    function_FishingForPlasmids2_2.function_FishingForPlasmids2_2(pFinder_output, EcPlGe_output, assembly_input, run, FFPrunDir, pmlst_output, FFP_output)
