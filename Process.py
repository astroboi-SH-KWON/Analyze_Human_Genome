

class Process:
    def __init__(self):
        self.tmp = ""
        self.ext_fa = ".fa"
        self.delimiter = "^"

    def split_by_element(self,tg_str,el):
        return str(tg_str).split(el)

    """
    :return
        tmp_dict = { GENE : [HGNC_ID] 
        , 'AARS': ['HGNC:20'], 'ABCE1': ['HGNC:69'], 'ABCF1': ['HGNC:70'], 'ACTB': ['HGNC:132']
        }
    """
    def make_ceg_dict(self, ceg_list):
        tmp_dict = {}
        null_arr = []
        for ceg_line in ceg_list:
            tmp_arr = ceg_line.split("\t")
            # remove NA data
            if tmp_arr[1] != 'NA':
                tmp_dict[tmp_arr[0]] = [tmp_arr[1]]
            else:
                null_arr.append(tmp_arr[0])
        return tmp_dict, null_arr

    """
    :return
        ceg_dict = { 'GENE': ['HGNC_ID', 'NMID']
        # , 'AARS': ['HGNC:20', 'NM_001605'], 'ABCE1': ['HGNC:69', 'NM_002940'], 'ABCF1': ['HGNC:70', ''] # remove key if NMID == ''
        , 'AARS': ['HGNC:20', 'NM_001605'], 'ABCE1': ['HGNC:69', 'NM_002940'], 'ACTB': ['HGNC:132', 'NM_001101']
        }
    """
    def add_nmid_by_hgnc_id(self, ceg_dict, hgnc_list, null_arr):
        rm_keys = []
        for key, val_arr in ceg_dict.items():
            for hgnc_line in hgnc_list:
                splt_arr = hgnc_line.split("\t")
                if val_arr[0] == splt_arr[0]:
                    # remove key and value if splt_arr[2] is null
                    if splt_arr[2] == '':
                        rm_keys.append(key)
                        null_arr.append(key)
                    else:
                        val_arr.append(splt_arr[2])
        for rm_key in rm_keys:
            ceg_dict.pop(rm_key)
        return ceg_dict, null_arr

    """
    :return
        ceg_dict = { 'GENE': ['HGNC_ID', 'NMID', hg38_ref_full, hg38_ref_full, ...]
        , 'AARS': ['HGNC:20', 'NM_001605', 'AARS\tNM_001605\tchr16\t-\t70252393\t7028...,70282784,70289509,']
        , 'ABCE1': ['HGNC:69', 'NM_002940', 'ABCE1\tNM_002940\tchr4\t+\t1450...5125101,145129524,']
        , 'ACTB': ['HGNC:132', 'NM_001101', 'ACTB\tNM_...', 'ACTB\tNM_...', 'ACTB\tNM_...'...]
        }
    """
    def add_hg38_ref_full(self, ceg_dict, hg38_list, null_gene_list):
        for key, val_arr in ceg_dict.items():
            count = 0
            for val in hg38_list:
                split_arr = val.split("\t")
                if split_arr[1] == val_arr[1]:
                    count = count + 1
                    val_arr.append(val)
            if count == 0:
                null_gene_list.append(key)
        return ceg_dict, null_gene_list

    """
    filter_out : chr19_GL949747v2_alt, chr19_* are not verified yet. 
                remove items if tmp_str in key[key.indexOf("^"):]
    :param
        dict = {
        'ZNF574^chr19': ['42076165', '42076286', '42078586', '42081552']
        , 'ABCE1^chr4': ['145098310', '145098419', '145104385', '145104515', '145105604', '145105690', '145108014', '145108112', '145109131', '145109249', '145110102', '145110240', '145110374', '145110444', '145110967', '145111064', '145112238', '145112328', '145117292', '145117414', '145119931', '145120153', '145121173', '145121233', '145121332', '145121391', '145123020', '145123131', '145123214', '145123357', '145123477', '145123600', '145124989', '145125101', '145127525', '145129524']
        , 'CNOT3^chr19_GL949746v1_alt': ['112590', '112822', '117777', '117852', '117967', '118035', '118290', '118365', '118508', '118598', '118854', '118983', '119085', '119181', '120446', '120666', '120758', '120892', '121449', '121506', '122995', '123383', '123467', '123591', '124407', '124606', '127075', '127175', '127277', '127476', '127716', '127849', '128564', '128690', '130158', '130531']
        , 'CNOT3^chr19_GL949747v2_alt': ['112590', '112822', '117777', '117852', '117967', '118035', '118290', '118365', '118508', '118598', '118854', '118983', '119085', '119181', '120446', '120666', '120758', '120892', '121449', '121506', '122995', '123383', '123467', '123591', '124407', '124606', '127075', '127175', '127277', '127476', '127716', '127849', '128564', '128690', '130159', '130532']
        ... }   
        , tmp_str : removed target string style             
    :return
        {'ZNF574^chr19': ['42076165', '42076286', '42078586', '42081552']
        , 'ABCE1^chr4': ['145098310', '145098419', '145104385', '145104515', '145105604', '145105690', '145108014', '145108112', '145109131', '145109249', '145110102', '145110240', '145110374', '145110444', '145110967', '145111064', '145112238', '145112328', '145117292', '145117414', '145119931', '145120153', '145121173', '145121233', '145121332', '145121391', '145123020', '145123131', '145123214', '145123357', '145123477', '145123600', '145124989', '145125101', '145127525', '145129524']
        , 'ACTB^chr7': ['5527147', '5527891', '5528003', '5528185', '5528280', '5528719', '5529160', '5529400', '5529534', '5529663', '5530523', '5530601']
        , 'CNOT3^chr19': ['54137761', '54137993', '54142928', '54143003', '54143118', '54143186', '54143441', '54143516', '54143659', '54143749', '54144005', '54144134', '54144236', '54144332', '54145597', '54145817', '54145909', '54146043', '54146600', '54146657', '54148147', '54148535', '54148619', '54148743', '54149559', '54149758', '54152225', '54152325', '54152427', '54152626', '54152866', '54152999', '54153714', '54153840', '54155308', '54155681']
        ...}
    """
    def filter_out(self, dict, tmp_str):
        tmp_dict = {}
        for key, val in dict.items():
            if tmp_str not in key[key.index("^"):]:
                tmp_dict[key] = val
        return tmp_dict

    """
    :return
        {
        '0ZNF574^chr19': ['42076165', '42076286', '42078586', '42081552']
        , '1ABCE1^chr4': ['145098310', '145098419', '145104385', '145104515', '145105604', '145105690', '145108014', '145108112', '145109131', '145109249', '145110102', '145110240', '145110374', '145110444', '145110967', '145111064', '145112238', '145112328', '145117292', '145117414', '145119931', '145120153', '145121173', '145121233', '145121332', '145121391', '145123020', '145123131', '145123214', '145123357', '145123477', '145123600', '145124989', '145125101', '145127525', '145129524']
        , '2CNOT3^chr19_GL949746v1_alt': ['112590', '112822', '117777', '117852', '117967', '118035', '118290', '118365', '118508', '118598', '118854', '118983', '119085', '119181', '120446', '120666', '120758', '120892', '121449', '121506', '122995', '123383', '123467', '123591', '124407', '124606', '127075', '127175', '127277', '127476', '127716', '127849', '128564', '128690', '130158', '130531']
        , '3CNOT3^chr19_GL949747v2_alt': ['112590', '112822', '117777', '117852', '117967', '118035', '118290', '118365', '118508', '118598', '118854', '118983', '119085', '119181', '120446', '120666', '120758', '120892', '121449', '121506', '122995', '123383', '123467', '123591', '124407', '124606', '127075', '127175', '127277', '127476', '127716', '127849', '128564', '128690', '130159', '130532']
        ... }
    """
    def get_exon_dixt(self, hg38_full_dict, hg38_strt):
        exon_dict = {}
        idx = 0
        for key, val_arr in hg38_full_dict.items():
            # len(val_arr) == hg38_strt if there is no exon index data in val_arr
            if len(val_arr) > hg38_strt: # 배열 중에 필요한 정보가 들어간 배열은 idx = HG38_START 이후에 정보가 있음. 배열 길이가 HG38_START 짧으면 정보 없어서 무시
                for tmp_str in val_arr[hg38_strt:]:
                    """
                    CNOT3	NM_014516	chr19	+	54137761	54155681	54142978	54155407	18	54137761,54142928,54143118,54143441,54143659,54144005,54144236,54145597,54145909,54146600,54148147,54148619,54149559,54152225,54152427,54152866,54153714,54155308,	54137993,54143003,54143186,54143516,54143749,54144134,54144332,54145817,54146043,54146657,54148535,54148743,54149758,54152325,54152626,54152999,54153840,54155681,
                    CNOT3	NM_014516	chr19_GL949746v1_alt	+	112590	130531	117827	130257	18	112590,117777,117967,118290,118508,118854,119085,120446,120758,121449,122995,123467,124407,127075,127277,127716,128564,130158,	112822,117852,118035,118365,118598,118983,119181,120666,120892,121506,123383,123591,124606,127175,127476,127849,128690,130531,
                    key : str(idx) + "CNOT3" + "^" + "chr19_GL949746v1_alt"
                    val : [exon1Start,exon1End,exon2Start,exon2End,exon3Start,exon3End ... ]
                    """
                    split_arr = tmp_str.split("\t")
                    tmp_list = []
                    start_sexon_arr = split_arr[9].split(",")
                    end_sexon_arr = split_arr[10].split(",")
                    for i in range(len(start_sexon_arr)):
                        if start_sexon_arr[i] != '':
                            tmp_list.append(start_sexon_arr[i])
                            tmp_list.append(end_sexon_arr[i])

                    exon_dict[str(idx)+key + self.delimiter + split_arr[2]] = tmp_list
                    idx = idx + 1
                    # exon_dict[split_arr[0] + "^" + split_arr[2]] = tmp_list
        return exon_dict

    def get_complementary(self, c):
        if c == 'C':
            return "G"
        elif c == 'A':
            return "T"
        elif c == 'T':
            return "A"
        elif c == 'G':
            return "C"
        elif c == 'N':
            return "N"
        else:
            print("get_complementary ERROR .... char is [" + c + "]")
            exit()

    """
    checkSeqByChar : match sequences by char with rules
    :param
        dna_char :
        rule_char : rules with "A", "C", "G", "T", "U", "N", "R",...
    :return
        boolean
    """
    def checkSeqByChar(self,dna_char, rule_char):
        flag = False
        if rule_char == 'N':
            return True
        elif rule_char in 'ACGTU':
            if dna_char == rule_char:
                return True
        elif rule_char == 'R':
            if dna_char in 'AG':
                return True
        # elif rule_char == 'r':
        #     if dna_char in 'CT':
        #         return True
        """
        add more rules of "ACTGU"
        """
        return flag


    def count_mismatch(self, i, dna_seq, rule_str, max_cnt, cnt):
        if len(dna_seq) == i:
            return cnt
        if cnt > max_cnt:
            return cnt
        if self.checkSeqByChar(dna_seq[i], rule_str[i]):
            return self.count_mismatch(i + 1, dna_seq, rule_str, max_cnt, cnt)
        else:
            return self.count_mismatch(i + 1, dna_seq, rule_str, max_cnt, cnt + 1)
    """
    match : match sequence with same length strings
    :param
        i : index of seq
        dna_seq : targeted DNA/RNA sequence 
        rule_str : rules with "ACGTU", "N", "R",...
    :return
        boolean
    """
    def match(self,i, dna_seq, rule_str):
        if len(dna_seq) == i:
            return True
        if self.checkSeqByChar(dna_seq[i], rule_str[i]):
            return self.match(i + 1, dna_seq, rule_str)
        else:
            return False

    def get_analysis2(self, exon_idx_dict, std_list, init_data):
        pam_seq_list = init_data[0]
        dir_path = init_data[1]
        max_mis_cnt = init_data[2]

        # tmp_count_dict = self.make_init_count_dict(init_data)
        # tmp_std_seq_dict = self.make_init_std_seq_dict2(std_list, tmp_count_dict)
        tmp_std_seq_dict = {}

        for key, exon_idx_val in exon_idx_dict.items():
            target_file_name = key[key.index(self.delimiter) + len(self.delimiter):] + self.ext_fa
            # TODO std_seq_list 원소 길이 모두 같은지, INITIAL_ANALYSIS[0][0]=PAM 길이 모두 같은지 확인하는 method 필요
            std_tot_len = len(std_list[0]) + len(pam_seq_list[0])

            with open(dir_path + target_file_name, "r") as f:

                header = f.readline()  # header ignored : >chr19
                print("header : " + header)

                idx = 0
                tmp_p_str = ""
                tmp_m_str = ""
                ex_itr_cnt = 0

                while True:
                    c = f.read(1)
                    if c == "":
                        break
                    if "\n" in c:
                        continue
                    elif "\r" in c:
                        continue

                    tmp_p_str = tmp_p_str + c.upper()
                    tmp_m_str = tmp_m_str + self.get_complementary(c.upper())

                    if len(tmp_p_str) > std_tot_len:
                        tmp_p_str = tmp_p_str[-std_tot_len:]
                        tmp_m_str = tmp_m_str[-std_tot_len:]

                    # check idx of "exon starts, intron ends" and "exon ends, intron starts"
                    if str(idx) in exon_idx_val:
                        ex_itr_cnt = ex_itr_cnt + 1
                        # the first initial char when exon or intron starts
                        tmp_p_str = tmp_p_str[-1:]
                        tmp_m_str = tmp_m_str[-1:]
                        # print("idx = " + str(idx) + ", tmp_str[" + tmp_p_str + "] ex_itr_cnt : " + str(ex_itr_cnt))
                    # the last exonEnds, loop out
                    if ex_itr_cnt == len(exon_idx_val):
                        break
                    if len(tmp_p_str) == std_tot_len:
                        if ex_itr_cnt > 0:
                            # exon starts, intron ends
                            if ex_itr_cnt % 2 != 0:
                                for pam in pam_seq_list:
                                    # check plus strand
                                    if self.match(0, tmp_p_str[-len(pam):], pam):
                                        # print("plus ["+tmp_p_str + "] idx = " + str(idx))
                                        for rule_str in std_list:
                                            cnt = self.count_mismatch(0, tmp_p_str[:-len(pam)], rule_str, max_mis_cnt, 0)
                                            if cnt <= max_mis_cnt:
                                                if rule_str in tmp_std_seq_dict:
                                                    if cnt in tmp_std_seq_dict[rule_str]:
                                                        tmp_std_seq_dict[rule_str][cnt].append(tmp_p_str)
                                                    else:
                                                        tmp_std_seq_dict[rule_str].update({cnt: [tmp_p_str]})
                                                else:
                                                    tmp_std_seq_dict[rule_str] = {cnt:[tmp_p_str]}

                                    # check minus strand
                                    if self.match(0, tmp_m_str[:len(pam)], pam[::-1]):
                                        # print("minu ["+tmp_m_str + "] idx = " + str(idx))
                                        for rule_str in std_list:
                                            cnt = self.count_mismatch(0, tmp_m_str[len(pam):], rule_str[::-1], max_mis_cnt, 0)
                                            if cnt <= max_mis_cnt:
                                                if rule_str in tmp_std_seq_dict:
                                                    if cnt in tmp_std_seq_dict[rule_str]:
                                                        tmp_std_seq_dict[rule_str][cnt].append(tmp_m_str)
                                                    else:
                                                        tmp_std_seq_dict[rule_str].update({cnt: [tmp_m_str]})
                                                else:
                                                    tmp_std_seq_dict[rule_str] = {cnt: [tmp_m_str]}

                            # exon ends, intron starts
                            else:
                                for pam in pam_seq_list:
                                    # check plus strand
                                    if self.match(0, tmp_p_str[-len(pam):], pam):
                                        # print("plus ["+tmp_p_str + "] idx = " + str(idx))
                                        for rule_str in std_list:
                                            cnt = self.count_mismatch(0, tmp_p_str[:-len(pam)], rule_str, max_mis_cnt,
                                                                      0)
                                            if cnt <= max_mis_cnt:
                                                if rule_str in tmp_std_seq_dict:
                                                    if cnt in tmp_std_seq_dict[rule_str]:
                                                        tmp_std_seq_dict[rule_str][cnt].append(tmp_p_str)
                                                    else:
                                                        tmp_std_seq_dict[rule_str].update({cnt: [tmp_p_str]})
                                                else:
                                                    tmp_std_seq_dict[rule_str] = {cnt: [tmp_p_str]}

                                    # check minus strand
                                    if self.match(0, tmp_m_str[:len(pam)], pam[::-1]):
                                        # print("minu ["+tmp_m_str + "] idx = " + str(idx))
                                        for rule_str in std_list:
                                            cnt = self.count_mismatch(0, tmp_m_str[len(pam):], rule_str[::-1],
                                                                      max_mis_cnt, 0)
                                            if cnt <= max_mis_cnt:
                                                if rule_str in tmp_std_seq_dict:
                                                    if cnt in tmp_std_seq_dict[rule_str]:
                                                        tmp_std_seq_dict[rule_str][cnt].append(tmp_m_str)
                                                    else:
                                                        tmp_std_seq_dict[rule_str].update({cnt: [tmp_m_str]})
                                                else:
                                                    tmp_std_seq_dict[rule_str] = {cnt: [tmp_m_str]}
                    idx = idx + 1
        return tmp_std_seq_dict
    
    # TODO total_exon_dict에 담는 로직 필요
    def get_analysis(self, exon_idx_dict, std_list, init_data):
        pam_seq_list = init_data[0]
        dir_path = init_data[1]
        max_mis_cnt = init_data[2]

        # tmp_count_dict = self.make_init_count_dict(init_data)
        # tmp_std_seq_dict = self.make_init_std_seq_dict(std_list, init_data, tmp_count_dict)
        # total_exon_dict = self.make_init_total_dict(exon_idx_dict, tmp_std_seq_dict)
        # total_intron_dict = self.make_init_total_dict(exon_idx_dict, tmp_std_seq_dict)

        # total_exon_dict = self.make_init_total_dict1(exon_idx_dict, std_list, init_data)
        # total_intron_dict = self.make_init_total_dict1(exon_idx_dict, std_list, init_data)

        total_exon_dict = {}
        total_intron_dict = {}
        for key, exon_idx_val in exon_idx_dict.items():
            key_exon_dict = {}
            key_intron_dict = {}
            target_file_name = key[key.index(self.delimiter) + len(self.delimiter):] + self.ext_fa
            # TODO std_seq_list 원소 길이 모두 같은지, INITIAL_ANALYSIS[0][0]=PAM 길이 모두 같은지 확인하는 method 필요
            std_tot_len = len(std_list[0]) + len(pam_seq_list[0])

            with open(dir_path + target_file_name, "r") as f:

                header = f.readline()  # header ignored : >chr19
                print("header : " + header)

                idx = 0
                tmp_p_str = ""
                tmp_m_str = ""
                ex_itr_cnt = 0

                while True:
                    c = f.read(1)
                    if c == "":
                        break
                    if "\n" in c:
                        continue
                    elif "\r" in c:
                        continue

                    tmp_p_str = tmp_p_str + c.upper()
                    tmp_m_str = tmp_m_str + self.get_complementary(c.upper())

                    if len(tmp_p_str) > std_tot_len:
                        tmp_p_str = tmp_p_str[-std_tot_len:]
                        tmp_m_str = tmp_m_str[-std_tot_len:]

                    # check idx of "exon starts, intron ends" and "exon ends, intron starts"
                    if str(idx) in exon_idx_val:
                        ex_itr_cnt = ex_itr_cnt + 1
                        # the first initial char when exon or intron starts
                        tmp_p_str = tmp_p_str[-1:]
                        tmp_m_str = tmp_m_str[-1:]
                        # print("idx = " + str(idx) + ", tmp_str[" + tmp_p_str + "] ex_itr_cnt : " + str(ex_itr_cnt))
                    # the last exonEnds, loop out
                    if ex_itr_cnt == len(exon_idx_val):
                        break
                    if len(tmp_p_str) == std_tot_len:
                        if ex_itr_cnt > 0:
                            # exon starts, intron ends
                            if ex_itr_cnt % 2 != 0:
                                for pam in pam_seq_list:
                                    # check plus strand
                                    if self.match(0, tmp_p_str[-len(pam):], pam):
                                        # print("plus ["+tmp_p_str + "] idx = " + str(idx))
                                        for rule_str in std_list:
                                            cnt = self.count_mismatch(0, tmp_p_str[:-len(pam)], rule_str, max_mis_cnt, 0)
                                            if cnt <= max_mis_cnt:
                                                total_exon_dict[key][rule_str + "+" + pam][cnt].append(tmp_p_str)
                                                print("")

                                    # check minus strand
                                    if self.match(0, tmp_m_str[:len(pam)], pam[::-1]):
                                        # print("minu ["+tmp_m_str + "] idx = " + str(idx))
                                        for rule_str in std_list:
                                            cnt = self.count_mismatch(0, tmp_m_str[len(pam):], rule_str[::-1], max_mis_cnt, 0)
                                            if cnt <= max_mis_cnt:
                                                total_exon_dict[key][rule_str + "-" + pam][cnt].append(tmp_m_str)
                                                print("")

                            # exon ends, intron starts
                            else:
                                for pam in pam_seq_list:
                                    # check plus strand
                                    if self.match(0, tmp_p_str[-len(pam):], pam):
                                        # print("plus ["+tmp_p_str + "] idx = " + str(idx))
                                        for rule_str in std_list:
                                            cnt = self.count_mismatch(0, tmp_p_str[:-len(pam)], rule_str, max_mis_cnt,
                                                                      0)
                                            if cnt <= max_mis_cnt:
                                                total_intron_dict[key][rule_str + "+" + pam][cnt].append(tmp_p_str)
                                                print("")

                                    # check minus strand
                                    if self.match(0, tmp_m_str[:len(pam)], pam[::-1]):
                                        # print("minu ["+tmp_m_str + "] idx = " + str(idx))
                                        for rule_str in std_list:
                                            cnt = self.count_mismatch(0, tmp_m_str[len(pam):], rule_str[::-1],
                                                                      max_mis_cnt, 0)
                                            if cnt <= max_mis_cnt:
                                                total_intron_dict[key][rule_str + "-" + pam][cnt].append(tmp_m_str)
                                                print("")
                    idx = idx + 1
            total_exon_dict[key] = key_exon_dict
            total_intron_dict[key] = key_intron_dict
        return total_exon_dict, total_intron_dict

    """
    :return
        {'0ZNF574^chr19': {
                        'GAATGGTTGTCAGAGTTTA+NRG': {0: [], 1: [], 2: [], 3: [], ... }
                        'GAATGGTTGTCAGAGTTTA-NRG': {0: [], 1: [], 2: [], 3: [], ... }
                        , 'AAGCCGTCCAGCGCAAACT+NRG': {0: [], 1: [], 2: [], 3: [], ... }
                        , 'AAGCCGTCCAGCGCAAACT-NRG': {0: [], 1: [], 2: [], 3: [], ... }
                        ...
                        , 'CATCACCTGCAGCCTGTTC-NRG': {0: [], 1: [], 2: [], 3: [], ... }
                        , 'ACTACGCCTCTGCCTTTCA+NRG': {0: [], 1: [], 2: [], 3: [], ... }
                        , 'ACTACGCCTCTGCCTTTCA-NRG': {0: [], 1: [], 2: [], 3: [], ... }
                        ...}}
    """
    def make_init_total_dict(self, exon_idx_dict, std_seq_dict):
        return {key: std_seq_dict for key in exon_idx_dict}

    def make_init_std_seq_dict(self, std_list, init_data, count_dict):
        pam_seq_list = init_data[0]
        std_seq_dict = {}
        for pam in pam_seq_list:
            for std_str in std_list:
                std_seq_dict[std_str + "+" + pam] = count_dict
                std_seq_dict[std_str + "-" + pam] = count_dict
        return std_seq_dict

    def make_init_count_dict(self,init_data):
        return {i: [] for i in range(init_data[2] + 1)}

    def make_init_total_dict1(self, exon_idx_dict, std_seq_dict, init_data):
        tmp_cnt_dict = {i: [] for i in range(init_data[2] + 1)}

        pam_seq_list = init_data[0]
        tmp_std_seq_dict = {}
        for pam in pam_seq_list:
            for std_str in std_seq_dict:
                tmp_std_seq_dict[std_str + "+" + pam] = tmp_cnt_dict
                tmp_std_seq_dict[std_str + "-" + pam] = tmp_cnt_dict

        return {key: tmp_std_seq_dict for key in exon_idx_dict}

    def make_init_std_seq_dict2(self, std_list, count_dict):
        std_seq_dict = {}
        for std_str in std_list:
            std_seq_dict[std_str] = count_dict
        return std_seq_dict












