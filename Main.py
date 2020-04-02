from time import clock

import Utils
import Process
############### start to set env ################
DIR_PATH = "D:/000_WORK/KimNahye/20200310/"

CEG_V2 = "CEGv2.txt"
HGNC_RE = "HGNC_Reference.txt"
HG38_RE = "hg38_refFlat_full.txt"
RAW_DATA_DIR = "hg38/Splited/"
HG38_START = 2 # 배열 중에 필요한 정보가 들어간 배열은 idx = HG38_START 이후에 정보가 있음. 배열 길이가 HG38_START 짧으면 정보 없어서 무시
MAX_MIS_CNT = 10 # mismatch 최대값

STD_SEQ = "guide_seq.xlsx"
SHEET_NAME = "Sheet2"
COL_NAME = "Guide (X20)"
PAM_SEQ = ['NRG']



INITIAL_ANALYSIS = [PAM_SEQ, DIR_PATH + RAW_DATA_DIR, MAX_MIS_CNT]
MAKE_EXCEL = [DIR_PATH, COL_NAME, MAX_MIS_CNT]
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

    exon_dict_no_filter = p.get_exon_dixt(hg38_full_dict, HG38_START)
    exon_idx_dict = p.filter_out(exon_dict_no_filter, "_")

    excel_dict = util.get_excel(DIR_PATH + STD_SEQ, SHEET_NAME)
    tmp_list = util.get_data_by_col(excel_dict, "Guide (X20)")
    # remove the first guide sequence ( for NaHye's project )
    std_seq_list = []
    for tmp_str in tmp_list:
        std_seq_list.append(tmp_str[1:])

    # total_exon_dict, total_intron_dict = p.get_analysis(exon_idx_dict, std_seq_list, INITIAL_ANALYSIS)
    total_dict = p.get_analysis2(exon_idx_dict, std_seq_list, INITIAL_ANALYSIS)
    util.make_excel1(MAKE_EXCEL, total_dict)


start_time = clock()
print("start >>>>>>>>>>>>>>>>>>")
main()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))
