from time import clock

import Utils
import Process
############### start to set env ################
DIR_PATH = "D:/000_WORK/KimNahye/20200310/"

CEG_V2 = "CEGv2.txt"
HGNC_RE = "HGNC_Reference.txt"
HG38_RE = "hg38_refFlat_full.txt"

HG38_START = 2



############### end setting env  ################

def main():
    util = Utils.Utils()
    p = Process.Process()

    hg38_full_dict = {'GENE': ['HGNC_ID', 'NMID']
        , 'ZNF574': ['HGNC:26166', 'NM_022752', 'ZNF574\tNM_022752\tchr19\t+\t42076165\t42081552\t42078606\t42081297\t2\t42076165,42078586,\t42076286,42081552,']
        , 'ABCE1': ['HGNC:69', 'NM_002940', 'ABCE1\tNM_002940\tchr4\t+\t145098310\t145129524\t145104412\t145127573\t18\t145098310,145104385,145105604,145108014,145109131,145110102,145110374,145110967,145112238,145117292,145119931,145121173,145121332,145123020,145123214,145123477,145124989,145127525,\t145098419,145104515,145105690,145108112,145109249,145110240,145110444,145111064,145112328,145117414,145120153,145121233,145121391,145123131,145123357,145123600,145125101,145129524,']
        , 'ACTB': ['HGNC:132', 'NM_001101', 'ACTB\tNM_001101\tchr7\t-\t5527147\t5530601\t5527747\t5529657\t6\t5527147,5528003,5528280,5529160,5529534,5530523,\t5527891,5528185,5528719,5529400,5529663,5530601,']
        , 'CNOT3': ['HGNC:7879', 'NM_014516',
                'CNOT3\tNM_014516\tchr19\t+\t54137761\t54155681\t54142978\t54155407\t18\t54137761,54142928,54143118,54143441,54143659,54144005,54144236,54145597,54145909,54146600,54148147,54148619,54149559,54152225,54152427,54152866,54153714,54155308,\t54137993,54143003,54143186,54143516,54143749,54144134,54144332,54145817,54146043,54146657,54148535,54148743,54149758,54152325,54152626,54152999,54153840,54155681,',
                'CNOT3\tNM_014516\tchr19_GL949746v1_alt\t+\t112590\t130531\t117827\t130257\t18\t112590,117777,117967,118290,118508,118854,119085,120446,120758,121449,122995,123467,124407,127075,127277,127716,128564,130158,\t112822,117852,118035,118365,118598,118983,119181,120666,120892,121506,123383,123591,124606,127175,127476,127849,128690,130531,',
                'CNOT3\tNM_014516\tchr19_GL949747v2_alt\t+\t112590\t130532\t117827\t130258\t18\t112590,117777,117967,118290,118508,118854,119085,120446,120758,121449,122995,123467,124407,127075,127277,127716,128564,130159,\t112822,117852,118035,118365,118598,118983,119181,120666,120892,121506,123383,123591,124606,127175,127476,127849,128690,130532,'
                    ]
                }

    exon_idx_dict = p.get_exon_dixt(hg38_full_dict, HG38_START)

    print(exon_idx_dict)







def check_dupl(list1,idx_list1 , list2, idx_list2):
    for line1 in list1:
        split_str = line1.split("\t")
        tmp_str = split_str[idx_list1]
        count = 0
        for line2 in list2:
            if tmp_str == line2.split("\t")[idx_list2]:
                count = count + 1
        if count != 1:
            print( split_str[0] + " : " + tmp_str + " >>> duple count : " +str(count))

def check_dupl2(dict ,idx_dict, list, idx_list):
    for key, val_arr in dict.items():
        count = 0
        for val in list:
            split_arr = val.split("\t")
            if split_arr[idx_list] == val_arr[idx_dict]:
                count = count + 1

        print("key ["+key+"] , count = "+str(count))

def check_exon_idx(exon_dict):
    for key, val_arr in exon_dict.items():
        print("key ::: "+key)
        for i in range(len(val_arr)):
            if i != 0:
                flag = False
                if val_arr[i-1] < val_arr[i]:
                    flag = True
                print(val_arr[i-1] + " < " + val_arr[i] + " ::: " +str(flag))



start_time = clock()
print("start >>>>>>>>>>>>>>>>>>")
main()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))