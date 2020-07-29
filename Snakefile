# Authors: Michael Visser and Moniek van Selst
# Date: 15-10-2018
# Last update: 25-07-2020

from os.path import join

configfile: "config.YAML"
wildcard_constraints:
    extension = config["file_extension"],
    run = config["run"]

rule all:
    input:
        FFP = expand("FFP_output/{run}/{run}_AssignedContigs.csv", run=config["run"]),
        # blastn_EcPlGe = expand("data/blast_EcPlGe/{run}.csv", run=config["run"]),
        # pmlst = expand("data/pmlst_out/{run}.csv", run=config["run"]),
        # blastn_pFinder = expand("data/blast_pFinder/{run}.csv", run=config["run"])

rule blastn_pFinder:
    input:
        "data/assemblyDir/{run}.{extension}"
    output:
        "data/blast_pFinder/{run}.csv"
    threads: 8
    shell:
        "blastn -query {input} -db blast_db/pFinder_db -out {output} -num_threads {threads} -perc_identity 95 -outfmt '6 qseqid sseqid pident length qcovs qstart qend sstart send evalue bitscore' -max_target_seqs 1 -max_hsps 1"

rule pmlst:
    input:
        assembly = "data/assemblyDir/{run}.{extension}",
        blast = "data/blast_pFinder/{run}.csv"
    output:
        dir = "data/pmlst_out/{run}/",
        file = "data/pmlst_out/{run}.csv"
    threads: 8
    run:
        from scripts import pmlst_script
        pmlst_script.pmlst(input.blast, input.assembly, output.dir, output.file)

rule blastn_EcPlGe:
    input:
        "data/assemblyDir/{run}.{extension}"
    output:
        "data/blast_EcPlGe/{run}.csv"
    threads: 8
    shell:
        "blastn -query {input} -db blast_db/EcPlGe_db -out {output} -num_threads {threads} -perc_identity 95 -outfmt '6 qseqid sseqid pident length qcovs qstart qend sstart send evalue bitscore' -max_target_seqs 5 -max_hsps 1 -qcov_hsp_perc 20"

rule FFP:
    input:
        contigs_vs_plasmidFinder = "data/blast_pFinder/{run}.csv",
        contigs_vs_EcPlGe = "data/blast_EcPlGe/{run}.csv",
        assembly = "data/assemblyDir/{run}.{extension}",
        pmlst = "data/pmlst_out/{run}.csv"
    output:
        # change path when moving folder
        outputDIR = expand("data/FFP_output/{{run}}/"),
        outFile = expand("data/FFP_output/{{run}}/{{run}}_AssignedContigs.csv")
    threads: 8
    run:
        import sys
        import os
        from scripts import function_FishingForPlasmids2_2

        sys.path.append(output.outputDIR)
        iso_name = str(output.outputDIR).split("/")
        isolate_name = iso_name[-2]
        print(isolate_name)
        print("--STARTING FishingForPlasmids-- for file:", input.assembly)

        function_FishingForPlasmids2_2.function_FishingForPlasmids2_2(
            input.contigs_vs_plasmidFinder, input.contigs_vs_EcPlGe, input.assembly, isolate_name, output.outputDIR, input.pmlst, output.outFile)
