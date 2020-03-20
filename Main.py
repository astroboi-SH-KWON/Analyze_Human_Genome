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
    # read data from DIR_PATH
    ceg_list = util.read_file_by_line_to_list(DIR_PATH + CEG_V2)
    hgnc_list = util.read_file_by_line_to_list(DIR_PATH + HGNC_RE)
    hg38_list = util.read_file_by_line_to_list(DIR_PATH + HG38_RE)

    p = Process.Process()
    ceg_dict, na_gene_list = p.make_ceg_dict(ceg_list)
    nmid_dict, null_gene_list = p.add_nmid_by_hgnc_id(ceg_dict, hgnc_list, na_gene_list)
    hg38_full_dict, null_gene_tot_list = p.add_hg38_ref_full(nmid_dict, hg38_list, null_gene_list)

    exon_idx_dict = p.get_exon_dixt(hg38_full_dict, HG38_START)


start_time = clock()
print("start >>>>>>>>>>>>>>>>>>")
main()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))
