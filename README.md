# FishingForPlasmids



Fishing For Plasmids

This repository contains a tool to fish plasmid contigs out of an Escherichia coli assembly. The Fishing For Plasmids tool tries to distinguish plasmid contigs from chromosome contigs and plasmid contigs from plasmid contigs, in case multiple plasmid types are present in the genome. The tool enables investigators to study plasmids based on E. coli WGS data.

Databases for the tool are hosted on figshare
https://figshare.com/articles/dataset/FishingForPlasmids_databases/12735692 

Installation

1. Git clone repository to wanted location
2. Obtain databases from Figshare and place them in the "blast_db" directory
3. Create a directory named “data” in this location
4. Create the following directories in the “data” directory: “assemblyDir”, “blast_EcPlGe”, “blast_pFinder”, “FFP_output”, “pmlst_out”
5. Create a directory named “pMLST” in the “scripts” directory

Dependencies

   Python 3.6 (or newer)
   blast (https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs)
   pmlst
   pmlst_db

Install pmlst and pmlst_db in the “pMLST” directory, you created in step 4, and follow installation protocol (https://bitbucket.org/genomicepidemiology/pmlst/src/master/)

Usage

1. Go to your Fishing For Plasmids directory in the terminal
2. Copy your assemblies of interest in the data/assemblyDir/ directory
Note: make sure all assemblies have the same file extension (.fna, .fa, or .fasta)
3. First create a config.YAML file by running:

    python script/make_config_file.py

4. Then run the FishingForPlasmids script:

    Python FFP.py

Note: The Snakefile is not functional yet, therefore, you have to use FFP.py    
