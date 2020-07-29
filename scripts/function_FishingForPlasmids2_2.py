# This is the new and improved FishingForPlasmids function
# It uses the following...
# ...inputfiles: contigs_vs_plasmidFinder (first hit, 95% identity), contigs_vs_EcPlGe (first 5 hits per contig), assembly
# ...never changing input: PlGe_vs_plasmidFinder (PlGe are the plasmids in the database ; input needed for PlGe_vs_pFinder_library)
# ...make Directories for these outputfiles: assigning_contigs.csv (outputDIR/scratchDIR/), several .fasta files (depending on the amount of plasmids, "plasmidFinder_list" outputDIR/)


def function_FishingForPlasmids2_2(contigs_vs_plasmidFinder, contigs_vs_EcPlGe, assembly, isolate_name, outputDIR,
                                   pmlst_out, assContigs):
    import sys

    print("--START-- FishingForPlasmids")
    # Al types that can be input of pMLST
    types = {"IncI1": "inci1", "IncHI1B": "inchi1", "IncHI1A": "inchi1",
             "IncA/C2": "incac", "IncAC2": "incac", "IncN": "incn", "IncHI2A": "inchi2",
             "IncHI2": "inchi2", "IncN2": "incn", "IncN3": "incn", "IncA/C": "incac",
             "IncFIA": "incf", "IncFIB": "incf", "IncFIC": "incf", "IncFII": "incf"}

    PlGe_vs_plasmidFinder = "blast_db/PlGe_vs_pFinder3.csv"

    sys.path.append(PlGe_vs_plasmidFinder)
    sys.path.append(contigs_vs_plasmidFinder)
    sys.path.append(contigs_vs_EcPlGe)
    sys.path.append(assembly)
    sys.path.append(outputDIR)
    sys.path.append(pmlst_out)

    # 1) Making of lists and dictionaries
    print("-- START -- creating lists and dictionaries")

    pmlst = {}
    try:
        with open(pmlst_out) as pmlst_o:
            print("pmlst open")
            pmlst_lines = pmlst_o.readlines()
    except IOError:
        print("cannot open contigs_vs_plasmidFinder:", contigs_vs_plasmidFinder)

    for line in pmlst_lines:
        print(line)
        subtype = line.split("\t")[1]
        type = subtype.split("-")[0]
        pmlst[type] = subtype
    print(pmlst)

    assigning_contigs = str(assContigs)
    # assigning_contigs = str(outputDIR) + str(isolate_name) + '_AssignedContigs.csv'
    # The a_count is an 'identifier', it will give a number to the assigned contigs (0 - 5)
    a_count = 0
    # The number tells you in which round the contig was assigned

    contig_list = []  # contigs that have been seen before will end up in this list
    assigned_list = []  # contigs that have a valid match end up in this list, when a contig is in this list it will be ignored
    # The two contigs lists are used to determine the unassigned contigsß
    plasmidFinder_list = []  # contigs_vs_plasmidFinder_list
    try:
        with open(contigs_vs_plasmidFinder) as cpf:
            cpf_lines = cpf.readlines()
    except IOError:
        print("cannot open contigs_vs_plasmidFinder:", contigs_vs_plasmidFinder)

    for line in cpf_lines:
        line = line.rstrip()
        cpf_words = line.split('\t')
        cpf_c_ID = cpf_words[0]  # contigID is the first word
        cpf_plasmidtype = cpf_words[1].replace('/', '').replace('(', '_').split(
            '_')  # second word is the plasmidFinder plasmid type
        cpf_ptype = cpf_plasmidtype[0]  # only part we need
        cpf_alength = cpf_words[3]  # allignment length is fourth word
        cpf_pflength = cpf_words[4]  # plasmidFinder length
        plasmidFinder_list.extend([cpf_ptype])
        # assign contig to plasmid in assigning_contigs.csv output
        try:
            with open(assigning_contigs, 'a') as out1:
                # hier aanpassen cfp_ptype
                if cpf_ptype in types:
                    cpf_ptype = types[cpf_ptype]
                    if cpf_ptype in pmlst:
                        cpf_ptype = pmlst[cpf_ptype]
                        cpf_ptype = cpf_ptype.rstrip()
                out1.write(str(a_count) + ';' + cpf_c_ID + ';' + cpf_ptype + '\n')
                # The a_count at the start, which is zero here, is the 'identifier'.
                # It shows that this contig was assigned by the pFinder blast
                contig_list.extend([cpf_c_ID])
                assigned_list.extend([cpf_c_ID])
        except IOError:
            print("cannot open assigning contigs file:", assigning_contigs)
    print("your assembly contains the following plasmids:", plasmidFinder_list)

    # PlGe_vs_pFinder_library
    PlGe_vs_pFinder_library = {}
    try:
        with open(PlGe_vs_plasmidFinder) as ppf:
            ppf_lines = ppf.readlines()
    except IOError:
        print("cannot open PlGe_vs_plasmidFinder:", PlGe_vs_plasmidFinder)

    for line in ppf_lines:
        line = line.rstrip()
        ppf_words = line.split('\t')
        ppf_p_ID = ppf_words[0]  # first word is the plasmid ID
        ppf_plasmidtype = ppf_words[1].replace('/', '').replace('(', '_').split(
            '_')  # second word is the plasmidFinder plasmid type
        ppf_ptype = ppf_plasmidtype[0]  # only part we need
        PlGe_vs_pFinder_library[ppf_p_ID] = ''
        PlGe_vs_pFinder_library[ppf_p_ID] = PlGe_vs_pFinder_library[ppf_p_ID] + ppf_ptype
    print("{plasmid database , pFinder plasmid type} library -- CREATED --")

    # assembly library
    assembly_library = {}
    try:
        with open(assembly) as ass:
            ass_lines = ass.readlines()
    except IOError:
        print("cannot open assembly file:", assembly)

    for line in ass_lines:
        line = line.rstrip()
        if line.startswith('>'):
            ass_words = line.split()
            ass_contig = ass_words[0][1:]  # skip first 'letter', the '>'
            assembly_library[ass_contig] = ''
        else:
            assembly_library[ass_contig] = assembly_library[ass_contig] + line
    print("{assembly contig , sequence} library -- CREATED --")
    print("creating lists and libraries -- END --")

    # 2) going trough the contigs_vs_EcPlGe blast file and assign contigs to either the chromosome or a plasmid type
    # It should not matter how many hits per contig are in the contigs_vs_EcPlGe blast file, due to a contig list that is created
    # the assigned contigs are written in the assigning_contigs file, which was made in L20

    print("-- START -- assigning contigs to chromosome or plasmid")
    print("assigned contigs can be found in the following output file:", assigning_contigs)

    try:
        with open(contigs_vs_EcPlGe) as cep:
            cep_lines = cep.readlines()
    except IOError:
        print("cannot open contigs_vs_EcPlGe blast file:", contigs_vs_EcPlGe)

    for line in cep_lines:
        line = line.rstrip()
        cep_words = line.split('\t')
        cep_contig = cep_words[0]
        cep_dbID = cep_words[1]  # dbID is database ID contains either chromosomeID or plasmidID
        cep_alength = cep_words[3]  # allignment length
        cep_clength = cep_words[4]  # contig length
        if cep_contig in assigned_list:
            a_count = 0
            continue
        else:
            a_count = a_count + 1
            if cep_contig in contig_list:
                if cep_dbID.startswith('pl_'):  # alle plasmiden in de db beginnen met pl_
                    for ppf_p_ID, ptype in PlGe_vs_pFinder_library.items():
                        if cep_dbID == ppf_p_ID:
                            if ptype in plasmidFinder_list:
                                try:
                                    with open(assigning_contigs, 'a') as out1:
                                        # hier aanpassen ptype
                                        if ptype in types:
                                            ptype = types[ptype]
                                            if ptype in pmlst:
                                                ptype = pmlst[ptype]
                                        out1.write(str(a_count) + ';' +
                                                   cep_contig + ';' + ptype + '\n')
                                except IOError:
                                    print("cannot open assigning contigs file:", assigning_contigs)
                                assigned_list.extend([cep_contig])
                                a_count = 0
                            else:
                                continue
                        else:
                            continue
                else:
                    try:
                        with open(assigning_contigs, 'a') as out1:
                            out1.write(str(a_count) + ';' + cep_contig + ';chromosome' + '\n')
                    except IOError:
                        print("cannot open assigning contigs file:", assigning_contigs)
                    assigned_list.extend([cep_contig])
                    a_count = 0
            else:
                contig_list.extend([cep_contig])
                a_count = 1
                if cep_dbID.startswith('pl_'):  # all plasmids in the database all start with pl_
                    for ppf_p_ID, ptype in PlGe_vs_pFinder_library.items():
                        if cep_dbID == ppf_p_ID:
                            if ptype in plasmidFinder_list:
                                try:
                                    with open(assigning_contigs, 'a') as out1:
                                        # hier ptype aanpassen
                                        if ptype in types:
                                            ptype = types[ptype]
                                            if ptype in pmlst:
                                                ptype = pmlst[ptype]
                                        out1.write(str(a_count) + ';' +
                                                   cep_contig + ';' + ptype + '\n')
                                except IOError:
                                    print("cannot open assigning contigs file:", assigning_contigs)
                                assigned_list.extend([cep_contig])
                                a_count = 0
                            else:
                                continue
                        else:
                            continue
                else:
                    try:
                        with open(assigning_contigs, 'a') as out1:
                            out1.write(str(a_count) + ';' + cep_contig + ';chromosome' + '\n')
                    except IOError:
                        print("cannot open assigning contigs file:", assigning_contigs)
                    assigned_list.extend([cep_contig])
                    a_count = 0

    print("assigning contigs to chromosome or plasmid -- END --")

    NotAssigned = set(contig_list)-set(assigned_list)

    try:
        with open(assigning_contigs, 'a') as out1:
            out1.write("7 --contigs that could not be assigned are:" + "\n7;" +
                       str(NotAssigned).replace("{", "").replace("}", "").replace("'", ""))
    except IOError:
        print("cannot open assigning contigs file:", assigning_contigs)

    print("-- contigs that could not be assigned are:", NotAssigned)

    # 3) Now fasta files will be made from the contigs that are assigned to a plasmidID
    print("-- START -- creating fasta files of plasmids")

    try:
        with open(assigning_contigs) as asc:
            asc_lines = asc.readlines()
    except IOError:
        print("cannot open assigned contigs file:", assigning_contigs)

    # hier plasmid finder list aanpasssen

    pFtypen = []
    for plasmid in plasmidFinder_list:
        if plasmid in types:
            plasmid = types[plasmid]
            if plasmid in pmlst:
                plasmid = pmlst[plasmid].rstrip()
        if plasmid not in pFtypen:
            pFtypen.append(plasmid)
    # print(pFtypen)
    for plasmid in pFtypen:
        output2 = str(outputDIR) + str(isolate_name) + "_" + plasmid + ".fasta"
        try:
            with open(output2, 'a') as out2:
                for line in asc_lines:
                    line = line.rstrip()
                    if int(line[0]) <= 6:
                        asc_words = line.split(';')
                        asc_contig = asc_words[1]
                        asc_type = asc_words[2]  # either chromosome or plasmid type
                        if asc_type == plasmid:
                            for ass_contig, seq in assembly_library.items():
                                if asc_contig == ass_contig:
                                    out2.write(">" + ass_contig + '\n' + seq + '\n')
                                else:
                                    continue
                        else:
                            continue
                    else:
                        continue
        except IOError:
            print("FAILED creating fasta file:", output2)
        print("plasmid fasta file CREATED:", output2)
    print("creating fasta files of plasmids -- END --")
    print("____________________________________________")
    print("-- Thank you for using FishingForPlasmids --")
