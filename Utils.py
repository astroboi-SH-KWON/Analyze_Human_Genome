

class Utils:
    def __init__(self):
        self.ext_txt = ".txt"

    def read_file_by_line_to_list(self,path):
        tmp_list = []
        with open(path, "r") as f:
            while True:
                tmp_line = f.readline().replace("\n", "")
                if tmp_line != '':
                    tmp_list.append(tmp_line)
                else:
                    break

        return tmp_list
