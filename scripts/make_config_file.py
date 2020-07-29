# Author: Michael Visser
# Snakefile only works if assemblyDir contains one file extension
# import directory functions
import os

workDir = os.getcwd()
assemblyDir = workDir + "/data/assemblyDir/"
confFile = workDir + "/config.YAML"

try:
    with open(confFile, "w") as conF:
        conF.write("# !! when using new files please utilize python makeconfig.py > config.yaml, this to ensure run with the new files!!" + "\n")
        conF.write("run:" + "\n")
        for file in os.listdir(assemblyDir):
            if file.endswith(".fna"):
                file_extension = "fna"
                conF.write("- " + file.split(".fna")[0] + "\n")
            elif file.endswith(".fa"):
                file_extension = "fa"
                conF.write("- " + file.split(".fa")[0] + "\n")
            elif file.endswith(".fasta"):
                file_extension = "fasta"
                conF.write("- " + file.split(".fasta")[0] + "\n")
            else:
                print("Unrecognized file extension. Supported file extensions are: .fna, .fa, and .fasta")
        print("config file created: ", confFile)
        conF.write("file_extension: " + file_extension)
except IOError:
    print("cannot create config file: ", confFile)
