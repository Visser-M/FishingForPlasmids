# Author: Moniek van Selst and Michael Visser
# Date: 15-10-2018
# Last update: 26-07-2020

import os

types = {"IncI1": "inci1", "IncHI1B": "inchi1", "IncHI1A": "inchi1",
         "IncA/C2": "incac", "IncAC2": "incac", "IncN": "incn", "IncHI2A": "inchi2",
         "IncHI2": "inchi2", "IncN2": "incn", "IncN3": "incn", "IncA/C": "incac",
         "IncFIA": "incf", "IncFIB": "incf", "IncFIC": "incf", "IncFII": "incf"}

def pmlst(input, assembly, output, outFile):
    isolate = str(input).split("/")[1]
    print(isolate)

    try:
        with open(input) as infile:
            inputlines = infile.readlines()
    except IOError:
        print("cannot open:", input)

    try:
        with open(outFile, "w") as out:
            for line in inputlines:
                line = line.rstrip()
                words = line.split('\t')
                type = words[1].split("_")[0].split("(")[0]
                if type in types:
                    command = "python scripts/pMLST/pmlst/pmlst.py -i " + assembly + " -o " + output + " -s " + types[type] + " -p scripts/pMLST/pmlst_db/ -t " + output + "temp/ -x"
                    print("--START-- pMLST for:", type)
                    os.system(command)
                    try:
                        with open(output + "results.txt") as results:
                            resultslines = results.readlines()
                    except IOError:
                        print("cannot open pmlst results.txt for:", isolate)

                    for rline in resultslines:
                        rline = rline.rstrip()
                        if rline.startswith("Sequence Type"):
                            sub = rline.split()[2]

                    pTYPE = types[type]
                    subtype =  pTYPE + "-ST" + sub

                    out.write(pTYPE + "\t" + subtype + "\n")
    except IOError:
        print("cannot open:", outFile)
